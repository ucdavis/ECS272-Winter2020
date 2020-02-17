import { Pokemon } from '../../consts/Pokemon';
import data from '../../data/data.json';

const getDomains = (targets: string[]) => {
  if (targets !== undefined) {
    const domains: Record<string, any> = targets.reduce((prev, curr) => {
      const t = data[0];
      if (typeof t[curr as keyof Pokemon] === typeof 0) {
        const array = data.map(item => item[curr as keyof Pokemon]) as number[];
        return {
          ...prev,
          [curr]: [Math.min(...array), Math.max(...array)]
        };
      } else {
        const array = data.map(item =>
          item[curr as keyof Pokemon] !== null
            ? item[curr as keyof Pokemon]!.toString()
            : ''
        );
        return {
          ...prev,
          [curr]: [
            ...Array.from(new Set(array)).sort((a, b) => (a < b ? -1 : 1))
          ]
        };
      }
    }, {});

    return domains;
  } else {
    return undefined;
  }
};

export default getDomains;
