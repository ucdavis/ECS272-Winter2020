# Constructing the dataset
## Each row in the dataFrame includes:
### image
 - dtype = `object`
 - image object of the visualization, created with the `Image` module from the `PIL` library
    - [See documentation here](https://pillow.readthedocs.io/en/stable/reference/Image.html)
### title
 - dtype = `string`
 - title of the chart/visualization
 - `None` if there is no title
### author
 - dtype = `string`
 - author of the Kaggle Kernel
### keywords
 - dtype = `list` of `string`
 - include details like type of plot, axis labels, caption, categorical vs numerical, discrete vs continuous, etc...
 - e.g. `["multiple plots", "histogram", "totals", "discrete", "numerical"]`
### features
 - dtype = `list` of `string`
 - chosen features/variables/dimensions that are visualized
 - make sure that you only put one or more of the column names
   **exactly as they are in the dataframe**
   - for instance, in the example below, the column being used is
     called `neighbourhood` and is the only feature being used in the
     visualization (because the other dimension is just a count)
### code
 - dtype = `string`
 - the actual line of code that generates the plot
 - remove references if possible (see example below)
 - e.g. `df.hist(edgecolor="black", linewidth=1.2, figsize=(30, 30));`
 - e.g. `sns.pairplot(df, height=3, diag_kind="hist")`
 - e.g. `sns.catplot("neighbourhood_group", data=df, kind="count",
   height=8)`
 
## Making the dataset
  Construct your dataFrame and use `pickle` to check the result into
  this directory with the name `jvanover_df`, `pouneh_df`, etc...

  **Be sure to filter by language and choose Python!**
  - Chitrabhanu looks at 1,5,9,...
  - Jackson looks at 2,6,10,...
  - Matt looks at 3,7,11,...
  - Pouneh looks at 4,8,12,...

## Example

### given the following kernel excerpt...


```
data = df.neighbourhood.value_counts()[:10]
plt.figure(figsize=(12, 8))
x = list(data.index)
y = list(data.values)
x.reverse()
y.reverse()

plt.title("Most Popular Neighbourhood")
plt.ylabel("Neighbourhood Area")
plt.xlabel("Number of guest Who host in this Area")

plt.barh(x, y)
```

![Figure
1](https://www.kaggleusercontent.com/kf/29232855/eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0..xvaFq1bUv-o-ODFkSwU3jA.s53lKk-nUJTcl3mPOeaaVTA8m_L-ieqB2rIm8flidCMQqneY7NmMu6GtlcdWoZsnm38g0Uj2ypC00k8BFKXN_PWEL-H_kDHqiELv305n63Dqe8zfv3hfUft429a5vewr8U1bmigC13cpFyGfznzIxLHHghkE4L2vRIL7pmfxzU8.3t0_eNnLzXHYy_e2d5OHyw/__results___files/__results___32_1.png)

### ...the dataFrame row representing the data point might look like:
```
{
    "image" : generatedImageObject,
    "title" : "Most Popular Neighbourhood",
    "author" : Jane Doe,
    "keywords" : ["bar chart", "counts", "categorical", "discrete", "Neighbourhood Area", "Number of guest Who host in this Area"],
    "features" : ["neighbourhood"],
    "code" : "plt.barh(list(data.index), list(data.values))"
}
```
