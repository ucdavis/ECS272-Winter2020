import { useState, useEffect } from 'react';
import { Pokemon } from '../../consts/Pokemon';
import data from '../../data/data.json';

type Props = { id?: number };

const useDetailsData = (props: Props) => {
  const [detailsData, setDetailsData] = useState<Pokemon | undefined>(
    undefined
  );

  useEffect(() => {
    if (props.id !== undefined) {
      setDetailsData(data.find(item => item.Number === props.id));
    }
  }, [props.id]);

  return detailsData;
};

export default useDetailsData;
