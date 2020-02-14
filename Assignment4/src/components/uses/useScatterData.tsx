import React, { useState, useEffect } from 'react';
import { Pokemon } from '../../consts/Pokemon';
import data from '../../data/data.json';
import { MarkSeriesPoint } from 'react-vis';
import clustering from '../../utils/clustering';
import { useApolloClient } from '@apollo/react-hooks';

type Props = { x?: string; y?: string; k: number };

const useScatterData = (props: Props) => {
  const client = useApolloClient();
  const [scatterData, setScatterData] = useState<MarkSeriesPoint[] | undefined>(
    undefined
  );

  useEffect(() => {
    if (props.x !== null && props.y !== null) {
      const array = data.reduce((prev, curr) => {
        const x = curr[props.x! as keyof Pokemon];
        const y = curr[props.y! as keyof Pokemon];
        if (x === null || y === null) return prev;
        return [
          ...prev,
          {
            id: curr.Number,
            name: curr.Name,
            x: x === false || x === true ? x.toString() : x,
            y: y === false || y === true ? y.toString() : y,
            size: 1
          }
        ];
      }, [] as MarkSeriesPoint[]);
      setScatterData(clustering(array, client, props.k));
    }
    return undefined;
  }, [client, props.k, props.x, props.y]);

  return scatterData;
};

export default useScatterData;
