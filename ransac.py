import open3d as o3d
import argparse
from geometric_features import prepare_dataset_v2, draw_registration_result

def parse_args():
    parser = argparse.ArgumentParser('Model')
    parser.add_argument('--voxel_size', type=float, default=0.05, help='size of the voxel to downsample')
    return parser.parse_args()



def execute_global_registration(source_down, target_down, source_fpfh,
                                target_fpfh, voxel_size):
    distance_threshold = voxel_size * 1.5
    print(":: RANSAC registration on downsampled point clouds.")
    print("   Since the downsampling voxel size is %.3f," % voxel_size)
    print("   we use a liberal distance threshold %.3f." % distance_threshold)
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
        4, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                0.9),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(4000000, 500))
    return result




if __name__ == '__main__':
    args = parse_args()
    voxel_size = args.voxel_size
    source, target, source_down, target_down, source_fpfh, target_fpfh = prepare_dataset_v2(
    voxel_size)
    result_ransac = execute_global_registration(source_down, target_down,
                                            source_fpfh, target_fpfh,
                                            voxel_size)
    print(result_ransac)
    draw_registration_result(source_down, target_down, result_ransac.transformation)


