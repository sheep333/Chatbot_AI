(function () {
    //------------------//
    //LearningModeの処理//
    //------------------//

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

    //予測をAjaxでPythonからとってくる
    function predictAnswer(sentence, f) {
        $.ajax({
            'url': predict_url,
            'data': {
                'sentence': sentence,
            },
            'dataType': 'text',
            'type':'GET',
        }).done(function (predict_data) {
            f(predict_data);
        })
    }

    //予測後の処理
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

    function dataPreserve() {
        $.ajax({
            'url': preserve_url,
            'data': {
                'exit': True,
            },
            'dataType': 'text',
            'type':'GET',
        }).done(() => {
            end()
        });
    }
    //プログラムを終了する処理
    function end() {
        botui.message.add({
            content: 'またね！'
        })
    }
})();