# Educational-website-and-courses-finder-for-keyword
Return the filtered useful educational resources based on input keyword and filtering conditions from users
## Functional Design(secondary version, subject to change)
### Module: DataCollection
1. Function: DataCollection
   - Description: The search process for resources gathering
   - Input:
     - keywords: list of keywords for related educational resources finding
   - Output:
     - raw_data: unprocessed related resources found through the search, stored in lists for future processing
   - Functionality: Obtain searching resources from Google Search with keywords

2. Function: Preprocessing(For classifier)
   - Description: Process the resources for later processing
   - Input:
     - raw_data: unprocessed related resources found through the search, stored in lists for future processing
   - Output:
     - processed_data: processed related resources found through the search, format friendly for later modules
   - Functionality: Turn the rough format of resources into the format and syntax that later modules want

### Module: UsefulnessRanking(This should be a large module, with many incoming supplement functions)
1. Function: ResourceRanking(Firstly implement by 'many-if')
   - Description: Rank the usefulness of collected resources
   - Input:
     - processed_data: processed related resources found through the search, format friendly for later modules
   - Output:
     - rank: a list that contains the ranking for resources of the same index in ripe_data accordingly
   - Functionality: Provide the ranking of usefulness for all resources, used as judgment criteria in later module

2. Function: FurtherResearch(extra)
   - Description: For each of the classified result, track some furthur features, include but not limited to user comments, user rankings, page view, share or reprint times, favorite perventage, release time, publisher etc..
   - Input:
     - processed_data: processed related resources found through the search, format friendly for later modules
     - (extra)conditions: filtering conditions for returned value according to user input string
   - Output:
     - filtered_data:  a list that contains the further ranking for resources of the same index in ripe_data accordingly
   - Functionality: Track all top results upon certain features for further usefulness evaluation

## Algorithm Design(secondary version, subject to change)
### (New version)only naive primary thought, no reference
1. Using a crawler to copy down the source code of html page for every individual google search result according to input keyword.</br>
![172eee9c7336938393c2ec712c2ff97](https://user-images.githubusercontent.com/66361320/135891667-90540080-ca48-456f-bb52-f97ef9aeb3da.png)

2. Judge usefulness based on the following features, every single point satisfied will add up score for that result, and different point may provide different score:</br>
![65fcdbba14250f5ec69c0f8a4c3a253](https://user-images.githubusercontent.com/66361320/137957846-cd0070b5-14ce-4db9-b9ce-49b44cf354d7.png)
   - (1) Whether the url of that result is ended with edu, org (Obviously not all resources are provided on .edu or .org, but this should give higher preference）
   - (2) The title label in html，such as'course', 'class' ,'lecture', 'tutorial', 'exercise', 'textbook', 'handout', 'guideline' etc.(But should all contain keyword)
   - (3) The 'audio','video','pdf' labels in html，a resource with picture or video or pdf can be much more useful than plain texts. 
      - Further judgement on the 'source' tag under 'video' tag or others, and check the 'src' string to fing out the name of audio, video or pdf to judge whether it is useful(based on the comparison to keyword)
      - Further judgement on the descriptive texts around the video, audio or pdf to find out how relevant it is to the keyword, rather than maybe an ad.
   - (4) Diagram, same as (3)

3. Some extra criteria I think is necessary(Planned extra implementation):
   - User comments, rankings, page view, share or reprint times, favorite perventage. 
   - Release time, publisher

### Detailed Implementation Steps
1. By doing manual work on the Internet, try to figure how well is for each existing feature, then modify or delete or supplement them
2. Complete basic implementation by combining crawler and many-if functions
3. Learn about how to build up and train a classifier, then fix step 2 into it.


## References
### Dataset
To be updated

### Papers
Blocked down paper, which might be useful for me but have no chance to read:https://ieeexplore.ieee.org/abstract/document/9529407
