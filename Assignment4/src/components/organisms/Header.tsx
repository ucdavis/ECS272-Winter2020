import React from 'react';
import { AppBar, Grid, Typography } from '@material-ui/core';
import classes from '*.module.css';

type Props = {};

const Header: React.FC<Props> = (props: Props) => {
  return (
    <AppBar
      position="sticky"
      style={{ backgroundColor: '#002855', height: '4rem' }}
    >
      <Grid container justify={'space-between'} alignItems={'center'}>
        <Typography variant="h6" style={{ margin: '1rem 3rem' }}>
          ECS272-2020 Assignment 4
        </Typography>
        <Typography variant="h4" style={{ margin: '0 3rem' }}>
          Po-K-Means
        </Typography>
        <Typography variant="body1" style={{ margin: '1rem 3rem' }}>
          Keita Makino, Alice Dagmar Helena Lundvall
        </Typography>
      </Grid>
    </AppBar>
  );
};

export default Header;
