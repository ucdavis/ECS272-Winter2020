import { useState, useEffect } from 'react';
import { Pokemon } from '../../consts/Pokemon';
import data from '../../data/data.json';

type Props = { id?: number };

const usePokemon = (props: Props) => {
  const [pokemon, setPokemon] = useState<Pokemon | undefined>(undefined);

  useEffect(() => {
    if (props.id !== undefined) {
      setPokemon(data.find(item => item.Number === props.id));
    }
  }, [props.id]);

  return pokemon;
};

export default usePokemon;
