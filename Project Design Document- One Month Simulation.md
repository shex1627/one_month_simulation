---
output: pdf_document
---
# Project Design Document: One Month Simulation

My project is a simulation game which players plan one month(31 days) of activities for the main charcter  
in the game. First I will explain roughly what the game is, then my general idea to implement it. I bold certain words because they are varibles, functions or objects in my implementation. If sentences start with symbol "#" means I may or may not implement the feature, or I am more likely to change it.

Although I try to use this game to somewhat model the behavoir of the real world but I also realize a simple model is no where near accurate.

## **The Game**
Each day, the player has certain amount of **will power** that he(for convenience, I will only use "he" instead of "he or she") could use for several activies: 
* do homework
* play games
* (physical) exercise
* sleep early
* rest 

The **goal** of this game is to finish all the homework in 31 days, progressing from 0% to 100%. ##each activity will consume a minimum amount of **will power** but the player can invest more **will power** for higer rewards. And the amount of rewarding attributes are determined by other attributes and a random variable generated from a function. In other others, holding everything else constant, performing **do homework** activity may increase the **Hw progress** ranging from 5 to 10 or 5 to 20. 

I will explain what each activity does:
### 1. do homework:
The **do homework** activity will increase the character's **homework progress** based on other variables:
* amount of **will power** invested 
* character's **competitiveness**

This actvity may *randomly* prompt an event that the character encounters a question that he does not know, then he will given the option to invest extra willpower to ask others for help. Then the character can choose whether to stop doing hw or invest more willpower to continue. #In both cases, investing extra will power will yield extra **homework progress**. 

### 2. play games
After selecting the **play games** activity, the player has the optional to invest more will power to become more engage in the games and receive more **competiveness** boost from the playing games activity

### 3. (physical) exercise
The **physical exercise** activity should consume more **will power** for higher **health** points. While **health** is below a certain amount, performing **physical exercise** will bring the status fatigue, which will decrease the **will power** regeneration for the next day. Higher **health** points can increase **base will power**.

### 4. sleep early and rest
The **rest** activity will increase the **day** by one, reseting the character's **will power** based on **health** and **sleep quality**, which can be boost by investing **will power** on the **sleeping early** activity. **Sleep early** activity does not activate the **rest** activity.

## **Implementation**   
The two main objects in my project will be the **Person** class for creating the main character and the **Activity** object. And all the sub-activities like **do homework** inherit from the **Activity** class.

And I also have to design a command parser.

The player chooses the main character's name and start the game,
At the begining of each day, the comman line window is going to print

"Hello, **character name**, this is day **day**, your willpower is **will power**, what would you like to do?
1 : do homework
2 : play games
3 : (physical) exercise
4 : sleep early
5 : rest 
"
At this stage, the player can input either integers from 1 to 5 or "status"

* inputting any one from 1 to 5 will prompt:
"How much will power would you like to spent on activity **Activity.name**, the minimum is **Activity.mini_willpower**"
After the player types in a float number, the main charcter will **.perform** the **activity**.

* status:
    "
    Competitiveness : **competiveness**
     health          : **health**
     sleep quality   : **sleep quality**
     remaining will power : **will power**
    "

* other inputs
  "invalid input, please try again**






