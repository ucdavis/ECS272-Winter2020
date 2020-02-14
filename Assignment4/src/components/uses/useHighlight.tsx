import { gql } from 'apollo-boost';
import { useQuery } from '@apollo/react-hooks';

const query = gql`
  {
    details {
      id
    }
  }
`;

const useHighlight = () => {
  const { data } = useQuery(query);

  return data.details.id;
};

export default useHighlight;
