import React from 'react';
import { Typography, Grid } from '@material-ui/core';
import Slider from '../atoms/Slider';
import { Props as SliderProps } from '../atoms/Slider';

type Props = SliderProps;

const SliderPanel: React.FC<Props> = (props: Props) => {
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
        alignItems={'center'}
      >
        <Grid item xs={2} sm={2} md={2} lg={2} xl={2}>
          <Typography variant={'body1'}>k</Typography>
        </Grid>
        <Grid item xs={10} sm={10} md={10} lg={10} xl={10}>
          <Slider {...props} />
        </Grid>
      </Grid>
    </>
  );
};

export default SliderPanel;
