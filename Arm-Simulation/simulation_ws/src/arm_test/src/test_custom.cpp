#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>
#include <moveit_msgs/DisplayRobotState.h>
#include <moveit_msgs/DisplayTrajectory.h>
#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>

int main(int argc, char **argv)
{
ros::init(argc, argv, "test_custom_node");
ros::NodeHandle node_handle;
ros::AsyncSpinner spinner(1);
spinner.start();
moveit::planning_interface::MoveGroupInterface group("arm");

moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

ros::Publisher display_publisher =
node_handle.advertise<moveit_msgs::DisplayTrajectory>
("/move_group/display_planned_path", 1, true);
moveit_msgs::DisplayTrajectory display_trajectory;
///Setting custom goal position
geometry_msgs::Pose target_pose1;
//target_pose1.orientation.w = 1.0;
target_pose1.position.x = 1.4;
target_pose1.position.y = 1.08;
target_pose1.position.z = 1.4;
group.setPoseTarget(target_pose1);
///Motion plan from current location to custom position
moveit::planning_interface::MoveGroupInterface::Plan my_plan;
bool success= static_cast<bool>(group.plan(my_plan));
group.setPlanningTime(45.0);
group.move();


ROS_INFO("Visualizing plan 1 (pose goal) %s",success?"":"FAILED");

/* Sleep to give RViz time to visualize the plan. */
sleep(5.0);
ros::shutdown();
return 0;
}
