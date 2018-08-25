(function () {
    //------------------//
    //LearningModeの処理//
    //------------------//

    //FIXME:ここらへんの処理はPythonでできるなら値だけJSONとかで渡したい
    //FIXME:できるだけ2次元配列処理ではなく、MapとかにしてO(1)で速さあげたい。
    //とはいえ、全ての行を一行ずつループ処理するならそんなかわらないかも？

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
            value:result[0],
            answer:result[1]
        }))
    }

    //BotUIを作成
    let botui = new BotUI('chat-app')
    let data = [] //ラベル配列用初期化

    botui.message.add({
        content: 'こんにちは!'
    }).then(init);

    //FIXME:promiseでちゃんと制御したい。
    function init() {
        return botui.action.text({
            delay: 1000,
            action: {
                placeholder: 'Enter your text here'
            }
        }).then(function (res) {
            sentence = res.value;
            predictAnswer(sentence, function(predict_content) {
                afterPredict(predict_content);
            })
        })
    }

    function afterPredict(predict_content) {
        botui.message.add({
            delay: 500,
            content: predict_content,
        }).then(function () {
            botui.message.add({
                delay: 500,
                content: 'まだ続けますか？'
            });
        }).then(function () {
            return botui.action.button({
                delay: 500,
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
                dataPreserve();
            }else{
                init();
            }
        });
    }

    function predictAnswer(sentence, f) {
        $.ajax({
            'url': predict_url,
            'data': {
                'sentence': sentence,
            },
            'dataType': 'text',
        }).done(function (predict_data) {
            f(predict_data);
        })
    }

    function dataPreserve() {
        $.ajax({
            'url': datapreserve_url,
            'data': {
                'exit': True,
            },
            'dataType': 'text',
        }).done({
            end();
        })
    }
    //プログラムを終了する処理
    function end() {
        botui.message.add({
            content: 'またね！'
        })
    }
})();