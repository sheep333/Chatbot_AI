$(function () {
    //------------------//
    //LearningModeの処理//
    //------------------//

    //FIXME:ここらへんの処理はPythonでできるなら値だけJSONとかで渡したい
    //FIXME:できるだけ2次元配列処理ではなく、MapとかにしてO(1)で速さあげたい。
    //とはいえ、一行ずつループ処理するならそんなかわらないかも？

    //CSVファイルを二次元配列([data,label]の配列)に変換
    function convertCSVtoArray(str) {
        let result = []
        let row = str.split("\n");

        for (let i = 0; i < row.length; i++) {
            result[i] = tmp[i].split(';')
        }
    }

    //CSVファイルをMap([data,label]の配列)に変換
    function convertCSVtoMap(str) {
        let result = []
        let row = str.split("\n");

        for (let i = 0; i < row.length; i++) {
            result[i] = tmp[i].split(';')
        }

        let answer_data = result.map((result_set, i) => ({
            value: result[0],
            answer:result[1]
        }))
    }

    //Twitterのデータファイル読み込み
    /*data_file = "data.csv"
    let req = new XMLHttpRequest();
    req.open("get", data_file);
    req.send(null)

    req.onload = function () {
        let dataset = convertCSVtoArray(req.responseText);
    }*/

    //Answerのデータファイル読み込み
    /*answer_file = "answer.csv"
    let req = new XMLHttpRequest();
    req.open("get", answer_file);
    req.send(null)

    req.onload = function () {
        let answerData = convertCSVtoMap(req.responseText);
    }*/

    //BotUIを作成
    let botui = new BotUI('chat-app')
    var data = [] //ラベル配列用初期化

    botui.message.add({
        content: 'こんにちは!'
    }).then(init);

    function init() {
        return botui.action.text({
            delay: 1000,
            action: {
                placeholder: 'Enter your text here'
            }
        }).then(function (res) {
            console.log(res);
            sentence = res.value;
            console.log(sentence);
            content = predictAnswer(sentence);
            console.log(content);
        }).then(function () {
            botui.message.add({
                delay: 200,
                content: content,
            });
        }).then(function () {
            botui.message.add({
                delay: 200,
                content: 'まだ続けますか？'
            });
        }).then(function () {
            return botui.action.button({
                delay: 200,
                action: [{
                    icon: 'circle-thin',
                    text: 'はい',
                    value: true
                }, {
                    icon: 'close',
                    text: 'いいえ',
                    value: false
                }]
            });
        }).then(function (res) {
            if (res.value == false) {
                for (let k = 0; k < data.length; k++) {
                    line_num = data[k][0];
                    data_file[line_num][1] = data[k][1];
                }
            }
        });
    }

    function predictAnswer(sentence) {
        $.ajax({
            'url': 'http://localhost:8000/predict/',
            'data': {
                'sentence': sentence,
            },
            'timeout': 10000,
            'dataType': 'text',
        })
        .done(function (data) {
            return data;
        })
    }

    //プログラムを終了する処理
    function end() {
        botui.message.add({
            content: 'またね！'
        })
    }
});