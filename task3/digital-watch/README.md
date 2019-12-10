### Task 3

Set python enviromnent with `source .env`

After environment has been set the project can be run with `svm digital-watch.des`

### Statechart

```STATECHART:
    Time [CS][DS]
      Run [DS]
      Stop 
    Light [CS][DS]
      On
      Off [DS]
    Chrono [CS][DS]
      On
      Off [DS]
    Refresh [CS][DS]
      Time [DS]
      Chrono
      Alarm
      Stop
    EditTime [CS] [DS]
      Off [DS]
      OffDelay
      On
      OnDelay
    Alarm [CS] [DS]
      Off [DS]
      OffDelay
      On
      OnDelay
```

#### Implemented features

* Time value being updated (1.)
* Background light (2.)
* Alternating between time and chrono (3.)
* Chrono itself (4.) (chrono is slowed down due to the restrictions of the program and doesn't update every 1/100th of a second.)
* The editing mode (5.)

#### Deficincies

* Alarm editing does not work properly, because the screen gets messy when trying to edit. (6.)
* Alarm itself doesn't alarm (6.)
* There is no feature for incrementing the time with buttons being held down. (7.)