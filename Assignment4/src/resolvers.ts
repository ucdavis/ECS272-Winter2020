import { gql } from 'apollo-boost';

export default {
  Mutation: {
    updateParallel: (
      _root: any,
      variables: { position: any; target: any },
      { cache, getCacheKey }: any
    ) => {
      const id = getCacheKey({
        __typename: 'parallel',
        id: 1
      });
      const fragment = gql`
        fragment targets on Parallel {
          title
          targets {
            position
            name
          }
        }
      `;
      const parallel = cache.readFragment({ fragment, id });
      const data = {
        title: parallel.title,
        targets: [
          ...parallel.targets.filter(
            (item: { position: any }) => item.position !== variables.position
          ),
          {
            position: variables.position,
            name: variables.target,
            __typename: 'target'
          }
        ].sort((a, b) => (a.position < b.position ? -1 : 1))
      };
      console.log(parallel);
      cache.writeData({ id, data });
      return null;
    }
  }
};
