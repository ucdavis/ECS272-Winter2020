import React from 'react';
import Select from 'react-select';
import { useApolloClient, useMutation } from '@apollo/react-hooks';
import { Slider as MuiSlider, makeStyles } from '@material-ui/core';

export type Props = { initial: number };

const useStyles = makeStyles({
  bar: {
    width: '100%',
    position: 'relative',
    zIndex: 0
  }
});

const Slider: React.FC<Props> = (props: Props) => {
  const client = useApolloClient();
  const handleChange = (_event: any, value: any) => {
    client.writeData({
      data: { scatter: { k: value, __typename: 'scatter' } }
    });
  };
  const classes = useStyles();

  return (
    <>
      <MuiSlider
        onChange={handleChange}
        className={classes.bar}
        max={8}
        min={1}
        defaultValue={props.initial}
        valueLabelDisplay={'on'}
      />
    </>
  );
};

export default Slider;
