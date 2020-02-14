import React, { useRef, useState, useEffect } from 'react';
import { XYPlot, LineSeries, DecorativeAxis, LabelSeries } from 'react-vis';
import useParallelData from '../uses/useParallelData';
import SelectorPanel from '../molecules/SelectorPanel';
import { Grid, makeStyles } from '@material-ui/core';
import useColor from '../uses/useColor';
import useHighlight from '../uses/useHighlight';
import { useWindowSize } from 'react-use';

export type Props = { targets: { position: number; name: string }[] };

const useStyles = makeStyles({
  selectorPanel: {
    height: 'calc(25vh - 1rem - 8px)'
  },
  parallel: {
    height: 'calc(75vh - 3rem - 24px)'
  }
});

const Parallel: React.FC<Props> = (props: Props) => {
  const classes = useStyles();
  const [parallelData, domains] = useParallelData({
    targets: props.targets
  });

  console.log(parallelData, domains);

  const ref = useRef<HTMLDivElement>(null);
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });

  const colors = useColor();
  const windowSize = useWindowSize();
  const highlight = useHighlight();

  useEffect(() => {
    setContainerSize({
      width: ref.current!.getBoundingClientRect().width,
      height: ref.current!.getBoundingClientRect().height
    });
  }, [windowSize]);

  return (
    <Grid
      item
      container
      xs={12}
      sm={12}
      md={12}
      lg={12}
      xl={12}
      className={'component'}
      alignContent={'space-around'}
    >
      <Grid
        item
        container
        xs={12}
        sm={12}
        md={12}
        lg={12}
        xl={12}
        alignContent={'space-around'}
        className={classes.selectorPanel}
      >
        {Array(6)
          .fill(0)
          .map((_i, index) => (
            <Grid item container xs={6} sm={6} md={6} lg={6} xl={6}>
              <SelectorPanel
                domain={'parallel'}
                target={`Axis ${index + 1}`}
                value={props.targets[index]?.name}
                position={index}
              />
            </Grid>
          ))}
      </Grid>
      <Grid
        item
        container
        xs={12}
        sm={12}
        md={12}
        lg={12}
        xl={12}
        ref={ref}
        className={classes.parallel}
        justify={'center'}
      >
        <XYPlot
          width={containerSize.width * 0.9}
          height={containerSize.height}
          xType="ordinal"
          margin={{ top: 15, left: 0, bottom: 15, right: 0 }}
        >
          {parallelData !== undefined
            ? parallelData!.map(
                (
                  item:
                    | (any[] | import('react-vis').LineSeriesPoint)[]
                    | undefined,
                  index: React.ReactText
                ) => {
                  return (
                    <LineSeries
                      data={item}
                      color={highlight === index ? '#222222' : colors[index]}
                      opacity={highlight === index ? 1 : 0.15}
                    />
                  );
                }
              )
            : null}
          {parallelData !== undefined
            ? parallelData![0].map(
                (item: { x: React.ReactText }, index: any) => {
                  return [
                    [
                      <DecorativeAxis
                        key={`${index}-axis`}
                        axisStart={{ x: item.x, y: 0 }}
                        axisEnd={{ x: item.x, y: 1 }}
                        axisDomain={[domains![item.x][0], domains![item.x][1]]}
                      />,
                      <LabelSeries
                        data={[
                          {
                            x: item.x,
                            y: -0.04,
                            label: item.x.toString(),
                            style: { fontSize: 14 }
                          }
                        ]}
                      />
                    ]
                  ];
                }
              )
            : null}
        </XYPlot>
      </Grid>
    </Grid>
  );
};

export default Parallel;
