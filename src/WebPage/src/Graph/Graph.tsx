// Plugin simpa pour le chartJS
// https://chartjs-plugin-datalabels.netlify.app/samples/scriptable/interactions.html
// https://github.com/AbelHeinsbroek/chartjs-plugin-crosshair
// https://github.com/Makanz/chartjs-plugin-trendline

import React, { useContext, useEffect, useRef } from "react";
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend,
	Decimation,
  } from 'chart.js';
import { Line, ChartJSOrUndefined } from 'react-chartjs-2';
import { defaultUpdatedValue, UpdatedValueContext } from "../API/UpdatedValue.tsx";
import { graphData } from "./GraphData.tsx";
import { graphOptions } from "./GraphOption.tsx";


function AddValueToDataSet(time: string, WaterLevel : number[], MotorSpeed : number[]) {
	graphData.labels?.push(time)
	graphData.datasets[0].data.push(WaterLevel[0] * 100)
	graphData.datasets[1].data.push(WaterLevel[1] * 100)
	graphData.datasets[2].data.push(WaterLevel[2] * 100)
	graphData.datasets[3].data.push(MotorSpeed[0] * 100)
	graphData.datasets[4].data.push(MotorSpeed[1] * 100)
}

export function Graph() : React.JSX.Element {

	ChartJS.register(
		CategoryScale,
		LinearScale,
		PointElement,
		LineElement,
		Title,
		Tooltip,
		Legend,
		Decimation
	);

	const ref = useRef<ChartJSOrUndefined<"line">>(null)

	const updatedValue = useContext(UpdatedValueContext)

	useEffect( () => {
		if(updatedValue === defaultUpdatedValue || ref.current == null) return
		AddValueToDataSet(updatedValue.time, updatedValue.WaterLevel, updatedValue.MotorSpeed)
		ref.current.data = graphData
		ref.current.update()

	}, [updatedValue, ref]  )

	return (
		<Line title="Title" ref={ref} options={graphOptions} data={graphData} />
	)
}