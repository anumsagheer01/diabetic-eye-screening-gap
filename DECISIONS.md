# Decisions

This file explains why I made each choice in this project. It's written so someone who has never worked in tech can follow it. Every entry has the same shape: what the problem was, what I looked at, what I picked, and why.

## Part 1: Setup

### Decision: Setting a spending alert before doing anything else

**What the problem is**
Cloud computing charges by the hour, like a taxi meter. If I start a powerful computer and forget to turn it off, the bill keeps growing. This is the most common way beginners get a surprise charge.

**The options I looked at**
I could set no limit and be careful. I could set an alert that emails me when spending crosses a line. Or I could avoid paid services completely.

**What I picked**
An alert at $20, with emails at 50%, 90%, and 100% of that amount.

**Why I picked it**
Being careful isn't a plan. Forgetting is easy. An alert costs nothing and takes five minutes. Avoiding paid services would have meant skipping the training part, which is a big part of what I wanted to learn.

**What this costs me**
Nothing, but I should be clear about what an alert can't do. It sends an email. It does not stop anything from running. So I also made rules for myself: stop the notebook every time I step away, and never leave a live prediction service running.

**What would change my mind**
If the free credits run out and I start paying real money, I'd lower the alert to match what I'm comfortable spending.

**Words used here, explained**
An alert is an automatic email. A live prediction service is a model that sits switched on around the clock waiting for requests, and it bills for every hour it's on, even if nobody uses it.

### Decision: Keeping everything in one place on the map

**What the problem is**
Google Cloud stores data in physical buildings in different parts of the world, and I have to pick where mine goes. A wrong pick can cause errors later or add small costs.

**The options I looked at**
I could put things in different places depending on the service. I could put everything in the United States.

**What I picked**
The bucket that holds the photos sits in a US data center called us-central1. The BigQuery dataset is set to "US", which covers the whole country.

**Why I picked it**
The free public datasets I plan to use are stored in the US. BigQuery only lets you combine two tables if they're stored in the same place, so my tables have to be in the US too. The photo bucket sits close to where the model training will run, which keeps things fast and avoids extra charges for moving data around.

**What this costs me**
Not much. The only downside is that these locations are fixed. If I ever wanted to move them, I'd have to copy everything over.

**What would change my mind**
If a dataset I need turns out to be stored somewhere else, I'd redo this part.

**Words used here, explained**
A data center is a building full of computers. A region is the area of the world where those buildings are.

### Decision: Keeping the GitHub page private until it's finished

**What the problem is**
Anything posted publicly can be seen by anyone. A half-finished project can give the wrong impression, and I also haven't yet checked whether every dataset allows sharing.

**The options I looked at**
Public from day one, or private until I'm ready.

**What I picked**
Private, and I'll switch it to public at the end.

**Why I picked it**
I want people to see the finished version, not the messy middle. It also gives me time to check each dataset's license before anything goes up.

**What this costs me**
Nobody can see my progress, and I can't share a link to ask for early feedback. If I want feedback, I can invite specific people.

**What would change my mind**
If I wanted to post about the project while it was still being built, I'd make it public earlier.

**Words used here, explained**
A repository, or repo, is a project folder on GitHub that keeps every version of every file, like a history book for the project.

### Decision: Keeping the data out of GitHub

**What the problem is**
Datasets are large, and some have rules about whether they can be re-shared.

**The options I looked at**
Uploading the data to GitHub, or leaving it out and explaining where to download it.

**What I picked**
I leave the data out. The README will list where each dataset came from and how to get it.

**Why I picked it**
It avoids breaking any license, keeps the repo small, and sends people to the original source, which is the right thing to do.

**What this costs me**
Someone wanting to rerun my work has to download the data themselves, which takes a little more effort.

**What would change my mind**
If a dataset's license clearly allowed sharing and it was small, I might include a tiny sample so the project is easier to try.

**Words used here, explained**
A license is the set of rules that says what you're allowed to do with someone else's data.
