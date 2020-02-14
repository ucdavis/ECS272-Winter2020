import React from 'react';
import logo from './logo.svg';
import './App.css';
import Index from './pages/Index';
import { Grid } from '@material-ui/core';

import ApolloClient, { InMemoryCache, gql } from 'apollo-boost';
import { ApolloProvider } from '@apollo/react-hooks';
import data from './data/initialState';
import resolvers from './resolvers';

const cache = new InMemoryCache();

const client = new ApolloClient({
  cache: cache,
  typeDefs: '',
  resolvers: resolvers
});

cache.writeData({
  data
});

const App = () => {
  return (
    <div className="App">
      <ApolloProvider client={client}>
        <Grid container xs={12} sm={12} md={12} lg={12} xl={12}>
          <Index />
        </Grid>
      </ApolloProvider>
    </div>
  );
};

export default App;
