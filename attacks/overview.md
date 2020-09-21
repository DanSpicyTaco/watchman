# Watchman Experiments - Overview

## Experimental Procedure

1. Find the Snort signature for the IDS and add it to the file
2. Start the flight plan
3. Run the attack
4. Move the logfile from the watchman to the simulation
5. Repeat 5 times

### Flight Plan

- In order to ensure consistency between experiments, an automated flight path was established
- The UAV would rise, then fly in a circle (more or less), then land

## Metrics

1. Asset capacity: the remainder of the asset after being attacked/compromised
   - Here, we define the asset as the software or hardware that we are trying to protect from attack
   - In this case, our assets are the UAV and watchman
   - We consider an asset to be damaged if a part of it has been damaged
   - This can only occur if the attack was successful, and the UAV has dropped out of the sky
   - Therefore, we mark 1 for a successful attack, 0 otherwise
2. Exploit probability: how easy it is to exploit a vulnerability
   - Marking guide:
     - Automation (3): how much of the process can be automated?
     - Availability (3): how much of the attack could be downloaded/used from packages on the internet
     - Accessibility (3): is there special hardware or software required to buy before launching the attack?
     - Timing (3): does it take longer than 1min for the attack to work?
   - Scale the mark to being out of 1
3. Network resilience: the percentage of compromised services that can be replaced/recovered by backup services
   - The service being attacked is the `uav.py` script
   - The only service that could replace it is the `watchman.py` script
   - Therefore, if the `watchman.py` script is unaffected by the attack, then mark 1, 0 otherwise
4. Operational capacity: the remaining capacity of a service after being affected by a direct attack
   - Of the two threads in `uav.py`, how many are still functioning after the attack?
   - 1 if 2 threads, 0.5 if 1 thread, 0 if no threads
5. Service availability: the availability of a required service to support a particular task
   - Can the UAV still operate after a reboot?

## Analysis

- Add the metrics (score/5) for each attempt of each attack
- Take the average result of each attempt
- Rank each of the attacks in terms of effectiveness

## Discussion

- The amount of time taken for the attack was not considered a lot
- Maybe for the future, we should have that as a bigger thing
- Services could have been over-represented
  - Measured the availability, capacity and resilience of the `uav.py` script
  - Capacity was not super relevant to measuring the effectiveness of the attack
- Network resilience was unfairly weighted towards the watchman architecture
- To account for this, the battery life, weight and processing power were also considered as separate metrics
- If the watchman channel was attacked, the system would break
