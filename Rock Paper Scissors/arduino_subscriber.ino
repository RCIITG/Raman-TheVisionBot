#include <ros.h>
#include <std_msgs/Int16.h>

ros::NodeHandle nh;

void subscriberCallback(const std_msgs::Int16& led_msg)
{
  if(led_msg.data == 1)
  {
    //code to make rock
  }
  else if(led_msg.data == 2)
  {
    //code to make paper
  }
  else
  {
    //code to make scissors
  }
}

ros::Subscriber<std_msgs::Int16> led_subscriber("toggle_led", &subscriberCallback);

void setup() {
  //setup the pin modes
  nh.initNode();
  nh.subscribe(led_subscriber);

}

void loop() {
  nh.spinOnce();
  delay(100);

}