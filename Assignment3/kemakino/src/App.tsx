import React from "react";
import "./App.css";
import Advanced from "./components/Advanced";

import ApolloClient from "apollo-boost";
import { ApolloProvider } from "@apollo/react-hooks";
import { InMemoryCache } from "apollo-cache-inmemory";
import Basic from "./components/Basic";

import data from "./data/data2.json";
import { makeStyles, AppBar, Grid, Typography, Box } from "@material-ui/core";

const cache = new InMemoryCache();
const client = new ApolloClient({ cache });

cache.writeData({
  data: {
    x: { value: "", __typename: "selection" },
    y: { value: "", __typename: "selection" },
    z: { value: "", __typename: "selection" },
    xt: { value: "", __typename: "selection" },
    zt: { value: "", __typename: "selection" }
  }
});

const useStyles = makeStyles({
  appBar: {
    backgroundColor: "#002855"
  },
  container: {
    fontFamily: "roboto, Arial, Helvetica, sans-serif !important",
    color: "#222",
    backgroundColor: "#FBF6E5",
    textAlign: "justify"
  },
  header: {
    margin: "5rem 0 1rem 0",
    padding: "0 3rem",
    borderBottom: "6px double #002855"
  },
  vis: {
    backgroundColor: "#F4E5B2",
    borderTop: "1px solid #DAAA00",
    borderBottom: "1px solid #DAAA00",
    margin: "1rem 0",
    padding: "1rem 3rem",
    "& .rv-xy-plot": {
      backgroundColor: "#FFFFFF"
    }
  }
});
const App: React.FC = () => {
  const classes = useStyles();

  return (
    <div className="App">
      <ApolloProvider client={client}>
        <AppBar position="sticky" className={classes.appBar}>
          <Grid container justify={"space-between"} alignItems={"center"}>
            <Typography variant="h5" style={{ margin: "1rem 3rem" }}>
              ECS272-2020 Assignment 3
            </Typography>
            <Typography variant="body1" style={{ margin: "1rem 3rem" }}>
              Keita Makino
            </Typography>
          </Grid>
        </AppBar>
        <Grid container className={classes.container} justify={"center"}>
          <Typography variant="h4" className={classes.header}>
            1: Crime Distribution in SF City
          </Typography>
          <Grid
            container
            item
            justify={"space-between"}
            className={classes.vis}
          >
            <Box width={"480px"}>
              <Typography variant={"body1"}>
                This hexgrid map displays the geographical distribution of
                crimes in San Francisco in 2016. By selecting the category and
                value, users can narrow down the selection of the data and see
                how crimes with a certain condition are located throughout the
                city.
              </Typography>
              <br />
              <Typography variant={"body1"}>
                When a user hovers mouse over a bin, it will display the number
                of crimes identified in the location. Also, clicking any bin
                with both category and value being set will narrow down the data
                which will be used in the next sunburst chart.
              </Typography>
              <br />
              <Typography variant={"body1"}>
                Also, users may trim the data by manipulating the slider. This
                is typically useful when there are some outliers in the map (as
                shown in the default view).
              </Typography>
            </Box>
            <Box width={"1280px"}>
              <Basic data={data as any[]} />
            </Box>
          </Grid>
          <Typography variant="h4" className={classes.header}>
            2: Crime Share in SF City
          </Typography>
          <Grid
            container
            item
            justify={"space-between"}
            className={classes.vis}
          >
            <Box width={"480px"}>
              <Typography variant={"body1"}>
                This sunburst chart illustrates the share of crimes under a
                certain condition in San Francisco city.
              </Typography>
              <br />
              <Typography variant={"body1"}>
                Selecting the first category will make a pie chart which
                displays the share of crimes with one condition. Then, users can
                get more detailed information by selecting the second category,
                which makes a two-layered pie chart (i.e., sunburst chart).
              </Typography>
              <br />
              <Typography variant={"body1"}>
                When a user hovers mouse onto an area of the chart, it will
                highlight the areas which has same parameter at the perimeter.
                It will be useful when a user want to compare the share of one
                attribute in different condition (e.g., comparison of the share
                of "assault" crimes over police districts).
              </Typography>
              <br />
              <Typography variant={"body1"}>
                The label at the center will give the size of the area currently
                hovered over, and the "path" which represents the current
                condition. The reset button will re-initialize the state of the
                visualization, including the first one.
              </Typography>
            </Box>
            <Box width={"1280px"}>
              <Advanced data={data as any[]} />
            </Box>
          </Grid>
        </Grid>
      </ApolloProvider>
    </div>
  );
};

export default App;
