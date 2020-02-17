# ecs272-2020-4

As a homework of [ECS272 2020 Winter: Immersive Visualization](https://github.com/ucdavis/ECS272-Winter2020).

# Webpage

You can try the demo [here](https://keita-makino.github.io/ecs272-2020-4).

# Workaround to Run Locally

You need to fix edit the typings of react-vis-types to enable labels in the parallel coordinates.

```ts
node_modules/react-vis-types/index.d.ts

...
- 122 x: number;
+ 122 x: number | string;
...
+ 514 numberOfTicks?: number;
...

```

# Data

[Pokemon dataset](https://www.kaggle.com/alopez247/pokemon)
