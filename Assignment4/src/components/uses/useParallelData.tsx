import { useState, useEffect } from 'react';
import { Pokemon } from '../../consts/Pokemon';
import data from '../../data/data.json';
import { LineSeriesPoint } from 'react-vis';
import useHighlight from './useHighlight';

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
    if (props.targets !== undefined) {
      const domains = targets.reduce((prev, curr) => {
        const array = data.map(item => item[curr as keyof Pokemon]) as number[];
        return {
          ...prev,
          [curr]: [Math.min(...array), Math.max(...array)]
        };
      }, {});

      setDomains(domains);

      if (domains !== undefined) {
        setParallelData(
          data.map(item => {
            return targets.reduce((prev, curr) => {
              return [
                ...prev,
                {
                  x: curr,
                  y:
                    ((item[curr as keyof Pokemon] as number) -
                      (domains as any)[curr][0]) /
                    ((domains as any)[curr][1] - (domains as any)[curr][0])
                }
              ];
            }, [] as LineSeriesPoint[]);
          })
        );
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [props.targets]);

  return [parallelData, domains];
};

export default useParallelData;
