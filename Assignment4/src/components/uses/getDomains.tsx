import { useState, useEffect } from 'react';
import { Pokemon } from '../../consts/Pokemon';
import data from '../../data/data.json';

const getDomains = (targets: string[]) => {
  if (targets !== undefined) {
    const domains: Record<string, any> = targets.reduce((prev, curr) => {
      const array = data.map(item => item[curr as keyof Pokemon]) as number[];
      return {
        ...prev,
        [curr]: [Math.min(...array), Math.max(...array)]
      };
    }, {});

    return domains;
  } else {
    return undefined;
  }
};

export default getDomains;
