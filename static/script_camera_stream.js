let source = new EventSource("/get_camera_stream"); //前端向flask的/get_camera_stream發送請求
source.onmessage = function (event) {

    //取得元素

    let timeDiv = document.getElementById("timeDiv");
    let tbody = document.getElementById('predictContainer');
    let totalPriceSpan = document.getElementById('totalPrice');
    let totalCaloriesSpan = document.getElementById('totalCalories');
    let totalProteinSpan = document.getElementById('totalProtein');
    let totalFatSpan = document.getElementById('totalFat');
    let totalCarbohydratesSpan = document.getElementById('totalCarbohydrates');
    let totalFiberSpan = document.getElementById('totalFiber');
    let camera_canvas = document.getElementById("main_camera");
    var ctx = camera_canvas.getContext("2d");
    let frame_data = JSON.parse(event.data)

    if (frame_data["image"] == "NC") {
        timeDiv.innerText = "相機未連線"
    } else {
        let timestamp = frame_data["timestamp"]
        let frame_base64 = frame_data["image"]
        let predict = frame_data["predict"]

        //更改數值

        var image = new Image();
        image.onload = function () {
            camera_canvas.width = image.naturalWidth
            camera_canvas.height = image.naturalHeight
            camera_canvas.style.aspectRatio = image.naturalWidth + "/" + image.naturalHeight
            ctx.drawImage(image, 0, 0);
            timeDiv.innerText = timestamp;

            // 清空之前的预测结果
            tbody.innerHTML = '';

            let totalPrice = 0;
            let totalCalories = 0;
            let totalProtein = 0;
            let totalFat = 0;
            let totalCarbohydrates = 0;
            let totalFiber = 0;

            // 添加每个选定的项目
            predict.selected_items.forEach(item => {
                // 创建新的表格行
                let row = document.createElement('tr');

                // 创建并设置每个单元格内容
                let nameCell = document.createElement('td');
                nameCell.textContent = item.name;
                row.appendChild(nameCell);

                let priceCell = document.createElement('td');
                priceCell.textContent = item.price + " 元";
                row.appendChild(priceCell);
                totalPrice += item.price;

                let caloriesCell = document.createElement('td');
                caloriesCell.textContent = item.calories;
                row.appendChild(caloriesCell);
                totalCalories += item.calories;

                let proteinCell = document.createElement('td');
                proteinCell.textContent = item.protein;
                row.appendChild(proteinCell);
                totalProtein += item.protein;

                let fatCell = document.createElement('td');
                fatCell.textContent = item.fat;
                row.appendChild(fatCell);
                totalFat += item.fat;

                let carbohydratesCell = document.createElement('td');
                carbohydratesCell.textContent = item.carbohydrates;
                row.appendChild(carbohydratesCell);
                totalCarbohydrates += item.carbohydrates;

                let fiberCell = document.createElement('td');
                fiberCell.textContent = item.fiber;
                row.appendChild(fiberCell);
                totalFiber += item.fiber;

                // 将新的行添加到表格的 tbody 中
                tbody.appendChild(row);
            });

            // 更新总价和总营养成分的显示
            totalPriceSpan.textContent = totalPrice.toFixed(2);
            totalCaloriesSpan.textContent = totalCalories.toFixed(2);
            totalProteinSpan.textContent = totalProtein.toFixed(2);
            totalFatSpan.textContent = totalFat.toFixed(2);
            totalCarbohydratesSpan.textContent = totalCarbohydrates.toFixed(2);
            totalFiberSpan.textContent = totalFiber.toFixed(2);
        };
        image.src = "data:image/png;base64," + frame_base64
        
        // 每隔2秒更新一次页面内容
        setInterval(updatePredict, 2000);
    }
    //source.close()
}
