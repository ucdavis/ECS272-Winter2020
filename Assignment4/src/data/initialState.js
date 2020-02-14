export default {
  scatter: {
    title: 'scatter',
    x: 'Attack',
    y: 'Defense',
    k: 2,
    __typename: 'scatter'
  },
  parallel: {
    id: 1,
    title: 'parallel',
    targets: [
      { position: 0, name: 'Attack', __typename: 'target' },
      { position: 1, name: 'Defense', __typename: 'target' }
    ],
    __typename: 'parallel'
  },
  details: {
    title: 'details',
    id: null,
    __typename: 'details'
  },
  colors: []
};
