#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: nosaka

import copy
import numpy as np
import open3d as o3d

def prepare_dataset(model, scene):
    '''
    @brief: 1. Read source and target pointclouds from .pcd or .ply
            2. Then downsampling is perfomed on both pointclouds
            3. Extract FPFH features from both pointclouds

    '''
    source = o3d.io.read_point_cloud(model)
    target = o3d.io.read_point_cloud(scene)
    
    voxel_size = np.abs((target.get_max_bound() - target.get_min_bound())).max() / 20 # /30
    
    # Open3D version "0.7.0" or lower
    #source_down = o3d.geometry.voxel_down_sample(source, voxel_size)
    #target_down = o3d.geometry.voxel_down_sample(target, voxel_size)

    #o3d.geometry.estimate_normals(source_down,
    #    o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size, max_nn = 30))
    #o3d.geometry.estimate_normals(target_down,
    #    o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size, max_nn = 30))

    # Open3D latest version("0.15.0") and surroundings (etc. 0.8.0)
    source_down = source.voxel_down_sample(voxel_size)
    target_down = target.voxel_down_sample(voxel_size)

    source_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(
        radius = voxel_size, max_nn = 30))
    target_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(
        radius = voxel_size, max_nn = 30))
   
    source_fpfh = o3d.registration.compute_fpfh_feature(source_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size, max_nn = 100))
    target_fpfh = o3d.registration.compute_fpfh_feature(target_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius = voxel_size, max_nn = 100))

    return source_down, target_down, source_fpfh, target_fpfh, voxel_size

def execute_global_registration(source_down, target_down, source_fpfh, target_fpfh, voxel_size):
    '''
    @brief: Calculate feature matching by RANSAC
            Point-To-Point is used for the RANSAC cost function

    '''
    distance_threshold = voxel_size

    return o3d.registration.registration_ransac_based_on_feature_matching(source_down, target_down,
            source_fpfh, target_fpfh,
            distance_threshold,
            o3d.registration.TransformationEstimationPointToPoint(), 4,
            [o3d.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
            o3d.registration.CorrespondenceCheckerBasedOnDistance(distance_threshold)],
            o3d.registration.RANSACConvergenceCriteria(max_iteration = 400000, max_validation = 5000))

def refine_registration(source, target, result_ransac, source_fpfh, target_fpfh, voxel_size):
    '''
    @brief: Refinement by ICP to further adjust alignment

    '''
    est_ptpln = o3d.registration.TransformationEstimationPointToPlane()
    criteria = o3d.registration.ICPConvergenceCriteria(max_iteration = 50)
    distance_threshold = voxel_size

    return o3d.registration.registration_icp(source, target,
            distance_threshold, result_ransac.transformation,
            est_ptpln, criteria)

def draw_registration_result(model, scene, trans):
    '''
    @brief: Visualize of source pointcloud transformed by matching and target pointcloud

    '''
    source = o3d.io.read_point_cloud(model)
    target = o3d.io.read_point_cloud(scene)

    source.paint_uniform_color([1, 0.706, 0])
    target.paint_uniform_color([0, 0.651, 0.929])

    source.transform(trans)
    o3d.visualization.draw_geometries([source, target])

def pose_decision_for_rotate_mat(result):
    '''
    @brief: Derive Roll, Pitch, and Yaw of Euler angles from rotation matrix and print it here!

    Hint: ZYX Euler angles aer generally used in Open3d and ROS

    '''
    pass

