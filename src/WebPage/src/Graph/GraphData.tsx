import { ChartData, ChartDataset } from "chart.js";
import { useContext } from "react";
import { BaseDataContext } from "../API/GetBaseData";

const commonDatasetoption : Partial<ChartDataset<"line">> = {
    pointRadius: 0, // Supprime les points
    fill: false,    // Remplis la zone sous la courbe
    // tension: 0.1,   // Rend la ligne fluid
}

export const graphData : ChartData<"line">  = {
    labels: [],
    datasets: [
        {
            label: 'Cuve 1 water level',
            borderColor: 'rgb(99, 219, 255)',
            backgroundColor: 'rgba(99, 219, 255, 0.5)',
            // yAxisID: 'WaterLevel',
            yAxisID: 'y',
            data: [],
            ...commonDatasetoption,
        },
        {
            label: 'Cuve 2 water level',
            // data: labels.map(() => Math.random() * 100),
            borderColor: 'rgb(99, 193, 255)',
            backgroundColor: 'rgba(99, 193, 255, 0.5)',
            // yAxisID: 'WaterLevel',
            yAxisID: 'y',
            data: [],
            ...commonDatasetoption,
        },
        {
            label: 'Cuve 3 water level',
            // data: labels.map(() => Math.random() * 100),
            borderColor: 'rgb(99, 148, 255)',
            backgroundColor: 'rgba(99, 148, 255, 0.5)',
            // yAxisID: 'WaterLevel',
            yAxisID: 'y',
            data: [],
            ...commonDatasetoption,
        },
        {
            label: 'Motor 1 Speed',
            // data: labels.map(() => Math.random() * 100),
            borderColor: 'rgb(92, 168, 73)',
            backgroundColor: 'rgba(92, 168, 73, 0.5)',
            // yAxisID: 'MotorSpeed',
            yAxisID: 'y',
            data: [],
            ...commonDatasetoption,
        },
        {
            label: 'Motor 2 Speed',
            // data: labels.map(() => Math.random() * 100),
            borderColor: 'rgb(51, 187, 39)',
            backgroundColor: 'rgba(51, 187, 39, 0.5)',
            // yAxisID: 'MotorSpeed',
            yAxisID: 'y',
            data: [],
            ...commonDatasetoption,
        },
    ],
};