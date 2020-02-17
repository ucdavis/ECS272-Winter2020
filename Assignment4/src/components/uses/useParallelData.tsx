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
      setParallelData(
        data.map(item => {
          return targets.reduce((prev, curr) => {
            const minMax = newDomains[curr];
            const key = curr as keyof Pokemon;
            return [
              ...prev,
              {
                x: curr,
                y:
                  typeof minMax[0] === typeof 1
                    ? ((item[key] as number) - minMax[0]) /
                      (minMax[1] - minMax[0])
                    : item[key] !== null
                    ? minMax.indexOf(item[key]!.toString()) /
                      (minMax.length - 1)
                    : minMax.indexOf('')
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
