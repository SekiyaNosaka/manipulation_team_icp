#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: nosaka

# General
import copy
import numpy as np
import open3d as o3d

# Self
from hackmodule import *

MODEL = "./data/bunny/model/bun_zipper.ply"
#MODEL = "./data/happy_buddha/model/happy_vrip.ply"
#MODEL = "./data/tuduki/model/knuckle_circle.pcd"

SCENE = "./data/bunny/scene/bun045.ply"
#SCENE = "./data/happy_buddha/scene/happyStandRight_24.ply"
#SCENE = "./data/tuduki/scene/knuckle_circle_env.pcd"

if __name__ == "__main__":
    # Downsampling and FPFH features caluculated for MODEL & SCENE
    source_down, target_down, source_fpfh, target_fpfh, voxel_size = prepare_dataset(MODEL, SCENE)

    # RANSAC calculation based on (Point-to-Point, FPFH, etc...)
    result_ransac = execute_global_registration(source_down, target_down,
        source_fpfh, target_fpfh, voxel_size)

    # ICP refinement of RANSAC calculation result
    result_icp = refine_registration(source_down, target_down,
        result_ransac, source_fpfh, target_fpfh, voxel_size)
    print("Rotation Matrix:  ", result_icp.transformation)

    # Let's spring values of Euler angles Roll, Pitch, Yaw
    pose_decision_for_rotate_mat(result_icp)

    # Visualization
    draw_registration_result(MODEL, SCENE, result_icp.transformation)

