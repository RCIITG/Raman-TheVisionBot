#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/robot_model_loader/robot_model_loader.h>
#include <moveit/robot_model/robot_model.h>
#include <moveit/robot_state/robot_state.h>

int main(int argc, char **argv)
{
ros::init(argc, argv, "test_random_node",ros::init_options::AnonymousName);
// start a ROS spinning thread
ros::AsyncSpinner spinner(1);
spinner.start();

robot_model_loader::RobotModelLoader robot_model_loader("robot_description");
  robot_model::RobotModelPtr kinematic_model = robot_model_loader.getModel();
 robot_state::RobotStatePtr kinematic_state(new robot_state::RobotState(kinematic_model));
  const robot_state::JointModelGroup* joint_model_group = kinematic_model->getJointModelGroup("arm");

  const std::vector<std::string>& joint_names = joint_model_group->getVariableNames();

// this connects to a running instance of the move_group node
// Here the Planning group is "arm"
moveit::planning_interface::MoveGroupInterface group("arm");
kinematic_state->setToRandomPositions(joint_model_group);
const Eigen::Isometry3d& end_effector_state = kinematic_state->getGlobalLinkTransform("link_06");

  /* Print end-effector pose. Remember that this is in the model frame */
  ROS_INFO_STREAM("Translation: \n" << end_effector_state.translation() << "\n");
// specify that our target will be a random one
group.setRandomTarget();
  

// plan the motion and then move the group to the sampled target
group.move();
ROS_INFO_STREAM("Translation: \n" << end_effector_state.translation() << "\n");
ros::waitForShutdown();
}