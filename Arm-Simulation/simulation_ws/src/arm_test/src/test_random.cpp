//MoveIt! header file
#include <moveit/move_group_interface/move_group_interface.h>
int main(int argc, char **argv)
{
ros::init(argc, argv, "test_random_node",ros::init_options::AnonymousName);
// start a ROS spinning thread
ros::AsyncSpinner spinner(1);
spinner.start();
// this connects to a running instance of the move_group node
// Here the Planning group is "arm"
moveit::planning_interface::MoveGroupInterface group("arm");
// specify that our target will be a random one
group.setRandomTarget();
// plan the motion and then move the group to the sampled target
group.move();
ros::waitForShutdown();
}