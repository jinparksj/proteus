# Proteus Robotic Lab Automation

* Idea on Proteus X-Y Plane as Top-view - IT IS JUST INTUITION from YOUTUBE CLIP about PROTEUS

![x_y_top_view](./img/x_y_top_view.png)

* DH Parameters

![dh parameters](./img/dh.png)

* Coordinates for Forward Kinematics

![kinematics](./img/kine.png)

    * Homogeneous Transformation Matrix

        HT from base to end effector

            = [0, 1, 0,            d2]

              [1, 0, 0,       a2 + d1]
              
              [0, 0, -1, a1 - d3 - d4]
              
              [0, 0, 0,             1]
              
* Inverse Kinematics
    * x = d2
    * y = a2 + d1
    * z = a1 - d3 - d4
    * d1 - joint 1, d2 - joint 2, d3 - joint 3, d4 - end-effector length
    
* GUI1: Choose Samples for Test

![gui1](./img/gui1.png)

* GUI2: Select Source and Target from Checked Samples

![gui2](./img/gui2.png)

* GUI3: Select Targeted Amount for Testing 

![gui3](./img/gui3.png)

* Simulation 1: Top View of Workspace 

![sim1](./img/simulation1.png)

* Simulation 2: Side View of Workspace 

![sim2](./img/simulation2.png)

