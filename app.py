# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, request
import openai
import tiktoken

app = Flask(__name__)

# 模型
ENGINE: str = os.environ.get('GPT_ENGINE') or 'text-chat-davinci-002-sh-alpha-aoruigiofdj83'

OPENAI_API_KEY: str = os.environ.get('OPENAI_API_KEY')

ENCODER = tiktoken.get_encoding('gpt2')


@app.route('/chat', methods=['POST'])
def chat():
    """
    发起聊天
    """
    messages = request.json.get('messages')

    if not OPENAI_API_KEY:
        return jsonify({
            'success': False,
            'status': {
                'code': 403,
                'message': 'OpenAI key 未设置'
            }
        })
    
    if not messages:
        return jsonify({
            'success': False,
            'status': {
                'code': 404,
                'message': '缺少参数'
            }
        })

    # 发起请求
    openai.api_key = OPENAI_API_KEY

    try:
        completion = openai.ChatCompletion.create(
            model=ENGINE,
            messages=messages,
            temperature=.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as err:
        return jsonify({
            'success': False,
            'status': {
                'code': 404,
                'message': str(err)
            }
        })
    
    # 返回结果
    return jsonify({
        'completion': completion,
        'success': True,
        'status': {
            'code': 200,
            'message': ' 请求成功'
        }
    })


@app.route('/test')
def say_hello(name: str = 'GPT'):
    return 'Hello, %s!' % name


if __name__ == '__main__':
    app.run()
