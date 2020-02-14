import { useState, useEffect } from 'react';
import { Pokemon } from '../../consts/Pokemon';
import data from '../../data/data.json';
import { LineSeriesPoint } from 'react-vis';
import getDomains from './getDomains';

type Props = { targets: { position: number; name: string }[] };

const useParallelData = (props: Props) => {
  const targets = props.targets.map(item => item.name);
  const [parallelData, setParallelData] = useState<
    LineSeriesPoint[][] | undefined
  >(undefined);
  const [domains, setDomains] = useState<Record<string, any> | undefined>(
    undefined
  );

  useEffect(() => {
    const newDomains = getDomains(targets);
    if (props.targets !== undefined && newDomains !== undefined) {
      console.log(newDomains);
      setParallelData(
        data.map(item => {
          return targets.reduce((prev, curr) => {
            return [
              ...prev,
              {
                x: curr,
                y:
                  ((item[curr as keyof Pokemon] as number) -
                    (newDomains as any)[curr][0]) /
                  ((newDomains as any)[curr][1] - (newDomains as any)[curr][0])
              }
            ];
          }, [] as LineSeriesPoint[]);
        })
      );
      setDomains(newDomains);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [props.targets]);

  return [parallelData, domains];
};

export default useParallelData;
