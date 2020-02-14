import React, { useRef, useState, useEffect } from 'react';
import { Typography, Grid, Box } from '@material-ui/core';
import useDetailsData from '../uses/useDetailsData';

export type Props = { id: number };

const Details: React.FC<Props> = (props: Props) => {
  const detailsData = useDetailsData({
    id: props.id
  });

  const ref = useRef<HTMLDivElement>(null);
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });

  let subset;
  let imgSrc;

  if (detailsData !== undefined) {
    subset = Object.entries(detailsData).filter(
      item =>
        item[0] === 'Number' ||
        item[0] === 'Name' ||
        item[0] === 'Type_1' ||
        item[0] === 'HP' ||
        item[0] === 'Attack' ||
        item[0] === 'Defense' ||
        item[0] === 'Sp_Atk' ||
        item[0] === 'Sp_def' ||
        item[0] === 'Speed' ||
        item[0] === 'Generation' ||
        item[0] === 'Height_m' ||
        item[0] === 'Weight_kg'
    );

    imgSrc =
      'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/' +
      subset.find(item => item[0] === 'Number')![1] +
      '.png';
  }

  useEffect(() => {
    console.log(ref.current);
    setContainerSize({
      width: ref.current!.getBoundingClientRect().width,
      height: ref.current!.getBoundingClientRect().height
    });
  }, []);

  return (
    <Grid
      item
      container
      xs={12}
      sm={12}
      md={12}
      lg={12}
      xl={12}
      style={{ height: 'calc(25vh - 1rem)' }}
      ref={ref}
      className={'component'}
      alignContent={'space-around'}
    >
      {subset !== undefined ? (
        <>
          <Grid
            item
            container
            xs={3}
            sm={3}
            md={3}
            lg={3}
            xl={3}
            justify={'center'}
            alignContent={'space-around'}
          >
            <img src={imgSrc} height={containerSize.height - 32}></img>
          </Grid>
          <Grid
            item
            container
            xs={3}
            sm={3}
            md={3}
            lg={3}
            xl={3}
            justify={'center'}
            alignContent={'space-around'}
          >
            {subset.slice(0, 2).map(([key, value]) => (
              <Grid
                item
                container
                xs={12}
                sm={12}
                md={12}
                lg={12}
                xl={12}
                direction={'column'}
              >
                <Typography variant={'h6'}>{key}</Typography>
                <Typography variant={'h3'}>{value?.toString()}</Typography>
              </Grid>
            ))}
          </Grid>
          <Grid
            item
            container
            xs={6}
            sm={6}
            md={6}
            lg={6}
            xl={6}
            justify={'center'}
            alignContent={'space-around'}
          >
            {subset.slice(2).map(([key, value]) => (
              <Grid item container xs={4} sm={4} md={4} lg={4} xl={4}>
                <Typography variant={'body1'}>
                  {key}: {value?.toString()}
                </Typography>
              </Grid>
            ))}
          </Grid>
        </>
      ) : (
        <Typography>
          Click any mark to show the details of a pokemon.
        </Typography>
      )}
    </Grid>
  );
};

export default Details;
