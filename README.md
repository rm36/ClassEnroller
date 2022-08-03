# ClassEnroller
Automates enrolling on a class right after getting an email that says there's availability

## Use Case
Imagine you're taking a master's at UIUC and you were very irresponsible because you didn't enroll in a class 6 months before it started. What now? Many people who enrolled in the class you want to take will drop it, and if you have set up notifications you might get an automated email telling you there's a spot available. One day, that happens. Hooray! You register for the class in 10 seconds but someone else was faster than you and your place is gone.. :(

There are 2 ways you can CS your way to getting a spot:
## 1. The "responsible" way
Here are the steps:
- i. You forward notification emails to a personal gmail account so you can use the Gmail API.
- ii. Follow the instructions in this [link](https://developers.google.com/gmail/api/guides/push#python) to set up subscriptions and permissions with Gmail.
- iii. You run the script that receives a notification whenever you get an email. You keep running the script until that happens. If it takes days, so be it, but make sure to login once daily to avoid getting stuck in 2FA. Once you get the email, the script will automate enrolling as fast as possible.

For step iii, make sure you change the IDs, credentials and more (marked as CHANGE_ME) in each script. This is how to run them:
```bash
> python create_inbox_watch.py
Called to subscribe to topic. Result: {...}

> python enroll_for_me.py
```

## 2. The other way
Why wait until you get the email? Just run enroller.py on an infinite loop! After all, electricity is way cheaper than any of these classes and the school's server (probably) won't block you after 100,000 requests.

## 3. What I did
Although I was also working on this to learn about Google Cloud APIs and how to automate web navigation, what ended up happening was that when I ran `enroller.py` to test the navigation, it ended up *actually* enrolling; a spot opened exactly at that time, before I got the email notification, and I never really had to use any of this. Such is life.
