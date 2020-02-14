/* eslint-disable @typescript-eslint/camelcase */
import React from 'react';
import { Grid, makeStyles } from '@material-ui/core';
import Scatter, { Props as ScatterProps } from '../organisms/Scatter';
import Details, { Props as DetailsProps } from '../organisms/Details';
import Parallel, { Props as ParallelProps } from '../organisms/Parallel';
import Header from '../organisms/Header';

type Props = {
  scatter: ScatterProps;
  details: DetailsProps;
  parallel: ParallelProps;
};

const useStyles = makeStyles({
  main: {
    height: 'calc(100vh - 4rem)',
    backgroundColor: '#FBF6E5'
  },
  scatter: {
    height: 'calc(68vh - 2.72rem)'
  },
  details: {
    height: 'calc(32vh - 1.28rem)'
  },
  parallel: {
    height: 'calc(100vh - 4rem)'
  },
  visBox: {
    boxShadow: 'inset 0 0 8px -3px #002855',
    '& .component': {
      padding: '16px'
    }
  }
});

const Index: React.FC<Props> = (props: Props) => {
  const classes = useStyles();

  return (
    <>
      <Grid item container xs={12} sm={12} md={12} lg={12} xl={12}>
        <Header />
      </Grid>
      <Grid
        item
        container
        xs={12}
        sm={12}
        md={12}
        lg={12}
        xl={12}
        className={classes.main}
      >
        {/* grid for scatter */}
        <Grid container item xs={12} sm={12} md={12} lg={8} xl={8}>
          <Grid
            container
            item
            xs={12}
            sm={12}
            md={12}
            lg={12}
            xl={12}
            className={`${classes.scatter} ${classes.visBox}`}
          >
            <Scatter {...props.scatter} />
          </Grid>
          <Grid
            container
            item
            xs={12}
            sm={12}
            md={12}
            lg={12}
            xl={12}
            className={`${classes.details} ${classes.visBox}`}
          >
            <Details id={props.details.id} />
          </Grid>
        </Grid>

        {/* grid for parallel & detail */}
        <Grid
          container
          item
          xs={12}
          sm={12}
          md={12}
          lg={4}
          xl={4}
          className={`${classes.parallel} ${classes.visBox}`}
        >
          <Parallel targets={props.parallel.targets} />
        </Grid>
      </Grid>
    </>
  );
};

export default Index;
