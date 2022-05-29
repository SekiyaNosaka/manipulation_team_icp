#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: nosaka

import numpy as np
import open3d as o3d

MODEL = "./data/bunny/model/bun_zipper.ply"
#MODEL = "./data/happy_buddha/model/happy_vrip.ply"
#MODEL = "./data/tuduki/model/~~.pcd"

SCENE = "./data/bunny/scene/bun045.ply"
#SCENE = "./data/happy_buddha/scene/happyStandRight_24.ply"
#SCENE = "./data/tuduki/scene/~~.pcd"

if __name__ == "__main__":
    source = o3d.io.read_point_cloud(MODEL)
    target = o3d.io.read_point_cloud(SCENE)

    o3d.visualization.draw_geometries([source, target])

