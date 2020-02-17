import React, { useRef, useState, useEffect } from 'react';
import { Typography, Grid, Box } from '@material-ui/core';
import usePokemon from '../uses/useDetailsData';
import { useWindowSize } from 'react-use';
import useParallelData from '../uses/useParallelData';
import { RadarChart, RadarChartPoint } from 'react-vis';
import getDomains from '../uses/getDomains';

export type Props = { id: number };

const Details: React.FC<Props> = (props: Props) => {
  const ref = useRef<HTMLDivElement>(null);
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });
  const windowSize = useWindowSize();
  const pokemon = usePokemon({
    id: props.id
  });

  const targets = ['HP', 'Attack', 'Defense', 'Sp_Atk', 'Sp_Def', 'Speed'];

  const domains = getDomains(targets);
  const params = targets.reduce(
    (prev, curr) => ({
      ...prev,
      [curr]: pokemon ? pokemon[curr as keyof typeof pokemon] : undefined
    }),
    {}
  );

  useEffect(() => {
    if (pokemon !== undefined) {
      setContainerSize({
        width: ref.current!.getBoundingClientRect().width,
        height: ref.current!.getBoundingClientRect().height
      });
    }
  }, [pokemon, windowSize]);

  const subset =
    pokemon !== undefined
      ? Object.entries(pokemon!).filter(item =>
          [
            'Number',
            'Name',
            'Type_1',
            'Type_2',
            'Generation',
            'Height_m',
            'Weight_kg'
          ].includes(item[0])
        )
      : undefined;

  const imgSrc = subset
    ? 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/' +
      subset.find(item => item[0] === 'Number')![1] +
      '.png'
    : undefined;

  return (
    <Grid
      item
      container
      xs={12}
      sm={12}
      md={12}
      lg={12}
      xl={12}
      ref={ref}
      className={'component'}
      alignContent={'space-around'}
    >
      {pokemon !== undefined ? (
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
            {subset?.slice(0, 2).map(([key, value]) => (
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
            xs={2}
            sm={2}
            md={2}
            lg={2}
            xl={2}
            justify={'center'}
            alignContent={'space-around'}
          >
            {subset?.slice(2).map(([key, value]) => (
              <>
                <Grid
                  item
                  container
                  xs={6}
                  sm={6}
                  md={6}
                  lg={6}
                  xl={6}
                  alignContent={'center'}
                >
                  <Typography variant={'subtitle2'}>{key}</Typography>
                </Grid>
                <Grid
                  item
                  container
                  xs={6}
                  sm={6}
                  md={6}
                  lg={6}
                  xl={6}
                  alignContent={'center'}
                >
                  <Typography variant={'h6'}>{value?.toString()}</Typography>
                </Grid>
              </>
            ))}
          </Grid>
          <Grid
            item
            container
            xs={4}
            sm={4}
            md={4}
            lg={4}
            xl={4}
            justify={'center'}
            alignContent={'space-around'}
          >
            <RadarChart
              margin={{ top: 40, right: 30, bottom: 30, left: 40 }}
              data={[params] as RadarChartPoint[]}
              height={containerSize.height - 32}
              width={containerSize.height - 32}
              domains={
                Object.entries(domains!).map(([key, value]) => ({
                  name: key,
                  domain: value
                })) as any
              }
            />
          </Grid>
        </>
      ) : (
        <Typography variant={'body1'}>
          Click any mark to show the details of the pokemon.
        </Typography>
      )}
    </Grid>
  );
};

export default Details;
