(function () {
    //BotUIを作成
    let botui = new BotUI('chat-app');
    var data = []; //ラベル配列用初期化
    let cnt = 0; //カウント用関数

    botui.messeage.bot({
        content: "こんにちは!"
    }).then(init);

    function init() {
        return botui.action.text({
            delay: 1000,
            action: {

            }
        }).then(function (res) {
            sentence = res.value;
            data[cnt][0] = sentence;
            //予測
            predictAnswer(sentence);
            botui.message.bot({
                loading: true
            }).then(function (index) {
                msgIndex = index;
            });
        })
        //ここに予測したあとの処理を追加

        botui.message.bot({
            delay: 200,
            content: 'まだ続けますか？'
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
                break;
            }
        })
    }

    //質問
    function predictAnswer(sentence) {
        $.ajax({
            url: '{% url "predict" %}',
            method: form.prop("method"),
            data: {
                sentence: sentence,
            },
            timeout: 10000,
            dataType: "text",
        })
        .done(function (data) {
            return data;
        })
    }

    //正解確認
    function dataLabeling(str, j) {
        botui.messeage.bot({
            delay: 200,
            content: str,
        }).then(function () {
            //正しい答えが入ってくるのをまつ
            return botui.action.select({
                placeholder: "Select Right Answer",
                value: 1,
                label: "label",
                options: answerData,
                button: {
                    icon: 'check',
                    label: 'OK'
                }
            })
        }).then(function (res) {
            //global変数にいれる
            data += [j, res.value]
        })
    }


    //プログラムを終了する処理
    function end() {
        botui.message.bot({
            content: 'またね！'
        })
    }
});