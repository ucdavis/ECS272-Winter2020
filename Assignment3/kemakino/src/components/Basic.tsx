import React, { useState } from "react";
import DeckGL from "@deck.gl/react";
import { HexagonLayer } from "@deck.gl/aggregation-layers";
import StaticMap from "react-map-gl";
import { useQuery, useApolloClient } from "@apollo/react-hooks";
import { gql } from "apollo-boost";
import rawData from "../data/data.json";
import lightingEffect from "../utils/lightingEffect";
import { makeStyles, Box, Grid, Typography, Slider } from "@material-ui/core";
import Selector from "./Selector";

type Props = { data: any[] };

const query = gql`
  query @client {
    x {
      value
      __typename
    }
    z {
      value
      __typename
    }
  }
`;

const material = {
  ambient: 0.4,
  diffuse: 0.8,
  shininess: 40,
  specularColor: [32, 48, 64]
};

const colorRange = [
  [1, 152, 189],
  [73, 227, 206],
  [216, 254, 181],
  [254, 237, 177],
  [254, 173, 84],
  [209, 55, 78]
];

const useStyles = makeStyles({
  map: {
    position: "relative",
    height: "720px"
  }
});

const Basic: React.FC<Props> = (props: Props) => {
  const client = useApolloClient();
  const classes = useStyles();
  const MAPBOX_TOKEN =
    "pk.eyJ1Ijoia2VtYWtpbm8iLCJhIjoiY2s1aHJkeWVpMDZzbDNubzltem80MGdnZSJ9.Mn_8DItICHFJyiPJ2rP_0Q";

  const [state, setState] = useState({
    hoveredObject: undefined,
    pointerX: 0,
    pointerY: 0
  });

  const [threshold, setThreshold] = useState(100);

  const { data } = useQuery(query);
  const plotData =
    data.z.value === ""
      ? props.data.map(item => ({ lat: Number(item.Y), lng: Number(item.X) }))
      : props.data
          .filter(
            item =>
              item[data.x.value as keyof typeof props.data[0]] === data.z.value
          )
          .map(item => ({ lat: Number(item.Y), lng: Number(item.X) }));

  const [view, setView] = React.useState({
    latitude: 37.74,
    longitude: -122.42,
    zoom: 12,
    pitch: 60,
    bearing: -30
  });

  const onHover = ({ object, x, y }: any) => {
    if (object === null) setState({ ...state, hoveredObject: undefined });
    else
      setState({
        hoveredObject: object,
        pointerX: x,
        pointerY: y
      });
  };

  const onClick = () => {
    if (data.x.value !== "" && data.z.value !== "") {
      client.writeData({
        data: {
          xt: {
            value: data.x.value !== "" ? data.x.value : "",
            __typename: "selection"
          },
          zt: {
            value: data.z.value !== "" ? data.z.value : "",
            __typename: "selection"
          }
        }
      });
    }
  };

  const hexagon = new HexagonLayer({
    id: "heatmap",
    colorRange,
    coverage: 0.9,
    data: plotData,
    pickable: true,
    elevationRange: [0, 250],
    elevationScale: 10,
    extruded: true,
    getPosition: (obj: { lng: any; lat: any }) => [obj.lng, obj.lat],
    radius: 100,
    upperPercentile: threshold,
    material: material,
    onHover: onHover,
    onClick: onClick
  });

  const handleChange = (_event: any, value: any) => {
    setThreshold(value);
  };

  return (
    <Box className={classes.map}>
      <DeckGL
        viewState={view}
        width={1280}
        height={720}
        layers={[hexagon]}
        effects={[lightingEffect]}
        controller
        onViewStateChange={({ viewState }) => setView(viewState)}
      >
        <StaticMap
          mapboxApiAccessToken={MAPBOX_TOKEN}
          width={960}
          height={600}
          mapStyle={"mapbox://styles/mapbox/dark-v9"}
        />
        {state.hoveredObject !== undefined ? (
          <div
            style={{
              position: "absolute",
              zIndex: 1,
              left: state.pointerX + 20,
              top: state.pointerY,
              padding: "0.5rem",
              backgroundColor: "#FFFFFF"
            }}
          >
            value: {(state.hoveredObject! as any).elevationValue}
          </div>
        ) : null}
      </DeckGL>
      <Grid
        container
        direction={"column"}
        style={{ position: "absolute", width: "240px", margin: "20px" }}
      >
        <Typography style={{ color: "white" }}>Category</Typography>
        <Selector data={props.data} target={"x"} />
        <br />
        <Typography style={{ color: "white" }}>Value</Typography>
        <Selector
          data={props.data}
          target={"z"}
          category={data.x.value !== "" ? data.x.value : undefined}
        />
        <br />
        <Typography style={{ color: "white" }}>Remove Outliers</Typography>
        <Slider
          defaultValue={100}
          max={100}
          min={80}
          onChange={handleChange}
          style={{ color: "#FFF2CC", width: "240px" }}
        />
      </Grid>
    </Box>
  );
};

export default Basic;
