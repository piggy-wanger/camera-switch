import React, { useState } from 'react';
import { Image, Space, Switch } from 'antd';
import axios from "axios";
import LoadPNG from './loading01.png';

interface CameraDisplayProps {
    cameraSwitchUrl: string;
}


const CameraDisplay: React.FC<CameraDisplayProps> = (props) => {
    const [cameraStatus, setCameraStatus] = useState(false);
    const [videoStream, setVideoStream] = useState(LoadPNG);

    const { cameraSwitchUrl } = props;

    const handleSwitchChange = async (checked: boolean) => {
        setCameraStatus(checked);
        axios.post(cameraSwitchUrl, {
            status: checked
        }).then(response => {

            if (checked) {
                if (response.data.result === 'success') {
                    console.log('后端响应:', response.data.message);
                    setVideoStream('/video');
                } else {
                    console.log('后端响应:', response.data.message);
                }
            } else {
                console.log('后端响应:', response.data.message);
                setVideoStream(LoadPNG);
            }

        }).catch(error => {
            console.error('发送数据到后端时出错:', error);
        })
    };

    return (
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Space direction='vertical' size='large'>
                <div>
                    <Image key={cameraStatus.toString()} src={ videoStream } preview={ false } height={ '480px' } width={ '640px' } />
                </div>

                <div style={{ display: 'flex', alignItems: 'center', float: 'right' }}>
                    <span style={{ marginRight: '24px' }}>相机开关</span>

                    <Switch checkedChildren='ON' unCheckedChildren='OFF' onChange={ handleSwitchChange } />
                </div>
            </Space>
        </div>
    )
};

export default CameraDisplay;