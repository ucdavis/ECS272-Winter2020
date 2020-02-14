import kmeans from 'ml-kmeans';
import { MarkSeriesPoint } from 'react-vis';
import { rgbToHex, hslToRgb } from '@material-ui/core';
import { ApolloClient } from 'apollo-boost';

const clustering = (
  data: MarkSeriesPoint[],
  client: ApolloClient<object>,
  k: number
) => {
  if (!Number(data[0].x) || !Number(data[0].y)) return;
  const array1 = data.map(item => item.x) as number[]; //from data find all variable1 values
  const array2 = data.map(item => item.y) as number[]; //from data find all variable2 values

  const centers = [];

  for (let index = 0; index < k; index++) {
    const x = Math.floor(
      Math.random() * Math.max(...array1) + Math.min(...array1)
    );
    const y = Math.floor(
      Math.random() * Math.max(...array2) + Math.min(...array2)
    );
    const center = [x, y];
    centers.push(center);
  }

  const chosendata = [];
  for (let index = 0; index < array1.length; index++) {
    chosendata.push([array1[index], array2[index]]);
  }

  const ans = kmeans(chosendata, k, { initialization: centers }).clusters;

  const getColor = (str: string | number) => {
    const hue = (str.toString().charCodeAt(0) * 147) % 360;
    return `hsl(${hue}, 75%, 60%)`;
  };

  const processedData = data.map((item, index) => ({
    ...item,
    color: rgbToHex(hslToRgb(getColor(ans[index]))),
    opacity: 0.25
  }));

  client.writeData({
    data: {
      colors: processedData.map(item => item.color)
    }
  });

  return processedData;
};

export default clustering;
