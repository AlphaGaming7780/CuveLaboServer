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
import { BaseDataContext } from "../API/GetBaseData.tsx";


function AddValueToDataSet(time: string, WaterLevel : number[], MotorSpeed : number[], numberOfCuve : number, numberOfMotor : number) {
	graphData.labels?.push(time)

	for(let i = 0; i < numberOfCuve; i++) {
		graphData.datasets[i].data.push(WaterLevel[i] * 100)
	}

	for(let i = 0; i < numberOfMotor; i++) {
		graphData.datasets[i + 3].data.push(MotorSpeed[i] * 100)
	} // The + 3 should be "+ numberOfCuve", but the graph is alway going to have 3 water level for now

	// graphData.datasets[0].data.push(WaterLevel[0] * 100)
	// graphData.datasets[1].data.push(WaterLevel[1] * 100)
	// graphData.datasets[2].data.push(WaterLevel[2] * 100)
	// graphData.datasets[3].data.push(MotorSpeed[0] * 100)
	// graphData.datasets[4].data.push(MotorSpeed[1] * 100)
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
	const { numberOfCuve, numberOfMotor } = useContext(BaseDataContext)

	useEffect( () => {
		if(updatedValue === defaultUpdatedValue || ref.current == null) return
		AddValueToDataSet(updatedValue.time, updatedValue.WaterLevel, updatedValue.MotorSpeed, numberOfCuve, numberOfMotor)
		ref.current.data = graphData
		ref.current.update()

	}, [updatedValue, ref, numberOfCuve, numberOfMotor]  )

	return (
		<Line title="Title" ref={ref} options={graphOptions} data={graphData} />
	)
}