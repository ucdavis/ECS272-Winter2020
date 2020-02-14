import { useState, useEffect } from 'react';
import { gql } from 'apollo-boost';
import { useQuery } from '@apollo/react-hooks';

const query = gql`
  {
    colors
  }
`;

const useColor = () => {
  const { data } = useQuery(query);

  return data.colors;
};

export default useColor;
