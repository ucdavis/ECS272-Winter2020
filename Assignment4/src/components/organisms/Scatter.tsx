import React, { useEffect, useRef, useState } from 'react';
import {
  XYPlot,
  XAxis,
  MarkSeries,
  YAxis,
  HorizontalGridLines,
  VerticalGridLines,
  MarkSeriesPoint,
  Hint
} from 'react-vis';
import useScatterData from '../uses/useScatterData';
import SelectorPanel from '../molecules/SelectorPanel';
import { Grid, Typography } from '@material-ui/core';
import { useApolloClient } from '@apollo/react-hooks';
import SliderPanel from '../molecules/SliderPanel';
import { useWindowSize } from 'react-use';
import useHighlight from '../uses/useHighlight';

export type Props = {
  title: string;
  x?: string;
  y?: string;
  k: number;
};

type ToolTip = {
  id: number;
  x: number;
  y: number;
  name: string;
};

const Scatter: React.FC<Props> = (props: Props) => {
  const client = useApolloClient();

  const ref = useRef<HTMLDivElement>(null);
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });
  const highlight = useHighlight();
  const scatterData = useScatterData({
    x: props.x,
    y: props.y,
    k: props.k
  })?.map(item => ({
    ...item,
    color: item.id === highlight ? '#222222' : item.color,
    opacity: item.id === highlight ? 1 : 0.25
  }));

  const tickValues =
    scatterData !== undefined
      ? {
          x:
            typeof scatterData[0].x !== 'number'
              ? [...Array.from(new Set(scatterData.map(item => item.x)))]
              : undefined,
          y:
            typeof scatterData[0].y !== 'number'
              ? [...Array.from(new Set(scatterData.map(item => item.y)))]
              : undefined
        }
      : { x: undefined, y: undefined };

  const [tooltip, setTooltip] = useState<ToolTip | undefined>(undefined);

  const onValueClick = (node: any, event: any) => {
    client.writeData({
      data: {
        details: {
          title: 'details',
          id: node.id,
          __typename: 'details'
        }
      }
    });
  };

  const windowSize = useWindowSize();

  const onMouseOver = (node: any, event: any) => {
    setTooltip({ x: node.x, y: node.y, id: node.id, name: node.name });
  };
  const onMouseOut = (node: any, event: any) => {
    setTooltip(undefined);
  };
  useEffect(() => {
    setContainerSize({
      width: ref.current!.getBoundingClientRect().width,
      height: ref.current!.getBoundingClientRect().height
    });
  }, [windowSize]);

  return (
    <Grid
      container
      item
      ref={ref}
      className={'component'}
      alignContent={'center'}
    >
      <Grid container item xs={8} sm={8} md={8} lg={8} xl={8}>
        {scatterData !== undefined ? (
          <XYPlot
            width={containerSize.width / 1.55}
            height={containerSize.height * 0.78}
            xType={tickValues.x !== undefined ? 'ordinal' : undefined}
            yType={tickValues.y !== undefined ? 'ordinal' : undefined}
            margin={{ left: tickValues.y !== undefined ? 60 : 40 }}
          >
            <HorizontalGridLines />
            <VerticalGridLines />
            <XAxis title={props.x} tickValues={tickValues.x} />
            <YAxis title={props.y} tickValues={tickValues.y} />
            <MarkSeries
              data={scatterData}
              onValueClick={onValueClick}
              strokeWidth={0.01}
              colorType="literal"
              onValueMouseOver={onMouseOver}
              onValueMouseOut={onMouseOut}
            />
            {tooltip !== undefined ? <Hint value={tooltip} /> : null}
          </XYPlot>
        ) : (
          <Typography>'Please select axes'</Typography>
        )}
      </Grid>

      <Grid
        container
        item
        xs={4}
        sm={4}
        md={4}
        lg={4}
        xl={4}
        justify="center"
        alignItems="center"
      >
        <SelectorPanel domain={'scatter'} target={'x'} value={props.x} />
        <SelectorPanel domain={'scatter'} target={'y'} value={props.y} />
        <SliderPanel initial={2} />
        {tickValues.x !== undefined || tickValues.y !== undefined ? (
          <Grid item container xs={10} sm={10} md={10} lg={10} xl={10}>
            <Typography variant={'body1'} color={'error'} align={'left'}>
              Clustering is not enabled as one or more variables are discrete.
            </Typography>
          </Grid>
        ) : null}
      </Grid>
    </Grid>
  );
};

export default Scatter;
