import React, { useState, useEffect, useRef } from "react";
import { Sunburst, LabelSeries } from "react-vis";
import * as NestHydrationJS from "nesthydrationjs";
import Selector from "./Selector";
import { gql } from "apollo-boost";
import { useQuery } from "@apollo/react-hooks";
import { Grid, Typography } from "@material-ui/core";
import Reset from "./Reset";

type Props = { data: any[] };

const query = gql`
  query @client {
    x {
      value
      __typename
    }
    y {
      value
      __typename
    }
    xt {
      value
      __typename
    }
    zt {
      value
      __typename
    }
  }
`;

const Advanced: React.FC<Props> = (props: Props) => {
  const ref = useRef(null);

  const [tooltip, setTooltip] = useState(["root"]);
  const [node, setNode] = useState<any>(false);
  const [highlights, setHighlights] = useState([] as string[]);

  const { data } = useQuery(query);
  const targetData =
    data.xt.value !== "" && data.zt.value !== ""
      ? props.data.filter(
          item =>
            item[data.xt.value as keyof typeof props.data[0]] === data.zt.value
        )
      : props.data;

  const nestedData = NestHydrationJS().nest(
    targetData.map((item: any) => {
      if (data.x.value === "") {
        return undefined;
      }
      let r;
      if (data.y.value === "") {
        r = {
          _id: item[data.x.value],
          _category: data.x.value,
          _children__id: item.IncidntNum,
          _children__size: 1,
          _children__treeEnd: true
        };
      } else {
        r = {
          _id: item[data.x.value],
          _category: data.x.value,
          _children__id: item[data.y.value],
          _children__category: data.y.value,
          _children__children__id: item.IncidntNum,
          _children__children__size: 1,
          _children__children__treeEnd: true
        };
      }
      return r;
    })
  );

  console.log(nestedData);

  const getFreqency = (item: any) => {
    return item.children.reduce(
      (prev: number, curr: any) => prev + curr.size,
      0
    );
  };

  const aggregate = (item: any) => {
    if (item === null) {
      return;
    }
    const hasGrandChildren = item[0].children[0].size !== undefined;
    const isTreeEnd = item[0].children[0].treeEnd;

    let r = item.map((item2: any) => ({
      id: item2.id,
      category: item2.category,
      children: isTreeEnd
        ? undefined
        : hasGrandChildren
        ? item2.children
        : aggregate(item2.children),
      color: getColor(item2.id),
      size: hasGrandChildren && isTreeEnd ? getFreqency(item2) : undefined,
      style: {
        fillOpacity: highlights.includes(item2.id) ? 1 : 0.25
      }
    }));

    console.log(r);
    if (r[0].size !== undefined) {
      r = r.sort((a: any, b: any) => (a.size > b.size ? -1 : 1));
    }

    if (r.length > 25) {
      r = r.slice(0, 25);
    }

    return r;
  };

  const getColor = (str: string | number) => {
    const hue = (str.toString().charCodeAt(0) * 255) % 360;
    return `hsl(${hue}, 75%, 60%)`;
  };

  let freqData = aggregate(nestedData);
  // while (freqData[0].size === undefined) freqData = aggregate(freqData);
  const plotData = {
    title: "root",
    category: "root",
    size:
      data.y.value !== ""
        ? freqData.reduce((prev: number, curr: any) => prev + curr.size, 0)
        : undefined,
    children: freqData,
    style: {
      fillOpacity: 0.2
    }
  };

  const getTooltip = (node: any): string[] => {
    if (node.parent === null) {
      return ["root"];
    } else {
      if (node.data) {
        return [
          `> ${node.data.category}<${node.data.id}>`,
          ...getTooltip(node.parent)
        ];
      } else {
        return [`> ${node.category}<${node.id}>`, ...getTooltip(node.parent)];
      }
    }
  };

  useEffect(() => {
    if (data.x.value === "" && data.y.value === "") setTooltip(["root"]);
  }, [data.x.value, data.y.value]);

  const onValueMouseOver = (node: any) => {
    const path = getTooltip(node);
    setNode(node);
    setTooltip(path.reverse());
    setHighlights(
      path
        .join("")
        .split("> ")
        .slice(1)
        .map(item => item.replace(/.*<(.*)>/g, "$1"))
    );
  };

  const onValueMouseOut = () => {
    setNode(false);
    setTooltip(["root"]);
    setHighlights([]);
  };

  console.log(node);

  return (
    <div ref={ref}>
      <Grid container>
        <Sunburst
          animation
          hideRootNode={data.x.value !== ""}
          data={plotData}
          width={1280}
          height={720}
          padAngle={0.005}
          onValueMouseOver={onValueMouseOver}
          onValueMouseOut={onValueMouseOut}
          style={{
            strokeOpacity: 0.6
          }}
        >
          {node !== false && node.id !== "root" ? (
            <LabelSeries
              data={[
                {
                  x: 0,
                  y: 0,
                  label:
                    node.size !== undefined
                      ? `size: ${node.size}`
                      : `size: ${getFreqency(node)}`,
                  yOffset: -40
                }
              ]}
              labelAnchorX={"middle"}
              style={{
                fontSize: "24px",
                backgroundColor: "white",
                padding: "20px",
                width: "360px"
              }}
            />
          ) : null}
          {tooltip.map((item, index) => (
            <LabelSeries
              data={[
                {
                  x: 0,
                  y: -(index + 1) * 20,
                  label: item,
                  yOffset: -20
                }
              ]}
              labelAnchorX={"middle"}
              style={{
                backgroundColor: "white",
                padding: "20px",
                width: "360px"
              }}
            />
          ))}
        </Sunburst>
        <Grid
          container
          item
          justify={"space-between"}
          direction={"column"}
          style={{
            height: "680px",
            position: "absolute",
            width: "240px",
            margin: "20px"
          }}
        >
          <Grid item direction={"column"}>
            <Typography>First-Category</Typography>
            <Selector data={props.data} target={"x"} />
            <br />
            <Typography>Second-Category</Typography>
            <Selector data={props.data} target={"y"} />
          </Grid>
          <Grid item>
            <Reset />
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
};

export default Advanced;
