#!/usr/bin/env python

import rospy
import click
import point_cloud_handler
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def treedcopy():
    pass

@treedcopy.command()
# add an option for output file
@click.option('-o', default='output.pcd', type=click.Path(exists=False), help='set output filename for scan')
# add a flag whether to open the file when scan is done
@click.option('-v', is_flag=True, help='if used, does not open a viewer after the scan is done')
@click.option('-f', is_flag=True, help='whether to run a fast scan or a precise scan')
def scan(**kwargs):
    """ Scan, register and mesh an object """
    rospy.wait_for_service('get_point_cloud')
    try:
        print("test1")
        get_point_cloud = rospy.ServiceProxy('get_point_cloud', point_cloud)
        print("test2")
        point_cloud = get_point_cloud()
        print("test3")
        print(point_cloud)
    except rospy.ServiceException, e:
        print("Service call failed: %s", e)

@treedcopy.command()
@click.option('-i', default='output.pcd', type=click.Path(exists=False), help='set input filename for mesh')
@click.option('-v', is_flag=True, help='if used, does not open a viewer after the scan is done')
@click.option('-f', is_flag=True, help='whether to run a fast scan or a precise scan')
def sar(**kwargs):
    """ Scan and register an object """
    pass

@treedcopy.command()
@click.option('-i', default='output.pcd', type=click.Path(exists=False), help='set input filename for mesh')
@click.option('-o', default='output.mesh', type=click.Path(exists=False), help='set output filename for mesh')
def mesh(**kwargs):
    """ Mesh a given object """
    rospy.wait_for_service('mesh_point_cloud')
    print("teste")
    try:
        if kwargs['i']:
            test = kwargs['i']
        print(test)
        mesh_point_cloud = rospy.ServiceProxy('mesh_point_cloud', point_cloud)
        generated_mesh = mesh_point_cloud()
        if kwargs['o']:
            test2 = kwargs['o']
        print(test2)
    except rospy.ServiceException, e:
        print("Service call failed: %s", e)

@treedcopy.command()
def reset(**kwargs):
    """ Reset the system and the hardware """
    os.system("treed reset -cart")
    os.system("treed reset -table 0")
    print("sup!")

def main():
    """
    Spins up the CLI.
    :return: None
    """
    rospy.init_node('3dcopy_cli', anonymous=False)
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
