# Assignment 1: Presentation of a Visualization

In this assignment, your task is to find a visualization that is "in the wild" somewhere out there on the Internet. Find what you believe is a good or interesting example of information visualization. Of course, since it's early in the quarter, and we haven't completely defined what makes a visualization "good," we don't expect you to find a flawless example, but do your best! You will then create a single HTML file to do the following:

* Show the title and your name in the HTML header
* Use a HTML img tag to show the image of the visualization (e.g. set the src property to be the hyperlink or URL of the image).
* Use css to modify the style of your HTML page where the visualization should be horizontally aligned to the middle of the page.
* Put the hyperlink to the source page that you got the visualization from.
* Write a short, text description of the visualization at the bottom.

Your text description should be a small paragraphs, and answer the following:
* What is being shown? (required)
* Is the visualization interactive or static? If interactive, how can it be interacted with?(required)
* What are some of the design choices and visualization techniques used? These include * things like choice of color or color palettes, the type of plot/chart used, the interaction techniques, etc.(optional)
* What, in your opinion, is the rationale behind the design choices? (optional)
* Do you think this is a good visualization? Give a short critique on why or why not. (required)

Your HTML page does not have to be elaborately styled, but please make it clean-looking and succinct.

You can use the ["example.html"](example.html) in this repository as the template for creating your html file.

For references on HTML and CSS, please refer to the [W3Schools HTML Tutorial](https://www.w3schools.com/html/default.asp) and [W3Schools CSS Tutorial](https://www.w3schools.com/css/default.asp).


## Submission
To submit for this assignment, you need to first fork this repository and add your html file to the submission folder. The name of your HTML file should be the same as your UC Davis email account name (without ' @ucdavis.edu'). After the fork, clone the forked repository using the following commands:

```bash
git clone https://github.com/<your-github-account-name>/ECS272-Winter2020
cd ECS272-Winter2020/Assignment1
mv <path-to-your-file> ./submission/
git add <your-filename> 
git commit -m "Assignment1"
git push
```

After you pushed your html file to your repository, follow the instruction [here](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) to create a pull request for this repository.

Finally, submit the hyper link of the pull request to UCD Canvas. The hyper link should look like - "https://github.com/ucdavis/ECS272-Winter2020/pull/{your-pull-request-id}".