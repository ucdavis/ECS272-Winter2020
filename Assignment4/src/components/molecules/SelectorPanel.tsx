import React from 'react';
import { Typography, Grid } from '@material-ui/core';
import Selector from '../atoms/Selector';
import { Props as SelectorProps } from '../atoms/Selector';

type Props = SelectorProps;

const SelectorPanel: React.FC<Props> = (props: Props) => {
  return (
    <>
      <Grid
        container
        item
        xs={12}
        sm={12}
        md={12}
        lg={12}
        xl={12}
        alignItems={'baseline'}
      >
        <Grid item xs={2} sm={2} md={2} lg={2} xl={2}>
          <Typography variant={'body1'}>{props.target}</Typography>
        </Grid>
        <Grid item xs={10} sm={10} md={10} lg={10} xl={10}>
          <Selector {...props} />
        </Grid>
      </Grid>
    </>
  );
};

export default SelectorPanel;
