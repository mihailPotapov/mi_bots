PGDMP                         |            bot_gpt    14.5    14.5 +               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    33672    bot_gpt    DATABASE     d   CREATE DATABASE bot_gpt WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Russian_Russia.1251';
    DROP DATABASE bot_gpt;
                postgres    false                       0    0    DATABASE bot_gpt    COMMENT     R   COMMENT ON DATABASE bot_gpt IS 'база данных для бота gpt_chat
';
                   postgres    false    3358            �            1259    33701    bot    TABLE        CREATE TABLE public.bot (
    id integer NOT NULL,
    name_bot character varying(255),
    nickname character varying(255)
);
    DROP TABLE public.bot;
       public         heap    postgres    false            �            1259    33700 
   bot_id_seq    SEQUENCE     �   CREATE SEQUENCE public.bot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 !   DROP SEQUENCE public.bot_id_seq;
       public          postgres    false    210                        0    0 
   bot_id_seq    SEQUENCE OWNED BY     9   ALTER SEQUENCE public.bot_id_seq OWNED BY public.bot.id;
          public          postgres    false    209            �            1259    33771 
   chat_roles    TABLE     x   CREATE TABLE public.chat_roles (
    id integer NOT NULL,
    id_chat bigint NOT NULL,
    id_roles integer NOT NULL
);
    DROP TABLE public.chat_roles;
       public         heap    postgres    false            �            1259    33770    chat_roles_id_seq    SEQUENCE     �   CREATE SEQUENCE public.chat_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.chat_roles_id_seq;
       public          postgres    false    216            !           0    0    chat_roles_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.chat_roles_id_seq OWNED BY public.chat_roles.id;
          public          postgres    false    215            �            1259    33756    roles    TABLE     m   CREATE TABLE public.roles (
    id_roles integer NOT NULL,
    name_roles character varying(255) NOT NULL
);
    DROP TABLE public.roles;
       public         heap    postgres    false            �            1259    33755    roles_id_roles_seq    SEQUENCE     �   CREATE SEQUENCE public.roles_id_roles_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 )   DROP SEQUENCE public.roles_id_roles_seq;
       public          postgres    false    214            "           0    0    roles_id_roles_seq    SEQUENCE OWNED BY     I   ALTER SEQUENCE public.roles_id_roles_seq OWNED BY public.roles.id_roles;
          public          postgres    false    213            �            1259    42001    tokens    TABLE     w   CREATE TABLE public.tokens (
    id integer NOT NULL,
    token integer DEFAULT 10000 NOT NULL,
    id_user integer
);
    DROP TABLE public.tokens;
       public         heap    postgres    false            �            1259    42000    tokens_id_seq    SEQUENCE     �   CREATE SEQUENCE public.tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.tokens_id_seq;
       public          postgres    false    218            #           0    0    tokens_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.tokens_id_seq OWNED BY public.tokens.id;
          public          postgres    false    217            �            1259    33710    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    name_user character varying(255),
    nickname_user character varying(255),
    id_chat bigint
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    33709    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public          postgres    false    212            $           0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
          public          postgres    false    211            p           2604    33704    bot id    DEFAULT     `   ALTER TABLE ONLY public.bot ALTER COLUMN id SET DEFAULT nextval('public.bot_id_seq'::regclass);
 5   ALTER TABLE public.bot ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    210    209    210            s           2604    33774    chat_roles id    DEFAULT     n   ALTER TABLE ONLY public.chat_roles ALTER COLUMN id SET DEFAULT nextval('public.chat_roles_id_seq'::regclass);
 <   ALTER TABLE public.chat_roles ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215    216            r           2604    33759    roles id_roles    DEFAULT     p   ALTER TABLE ONLY public.roles ALTER COLUMN id_roles SET DEFAULT nextval('public.roles_id_roles_seq'::regclass);
 =   ALTER TABLE public.roles ALTER COLUMN id_roles DROP DEFAULT;
       public          postgres    false    214    213    214            t           2604    42004 	   tokens id    DEFAULT     f   ALTER TABLE ONLY public.tokens ALTER COLUMN id SET DEFAULT nextval('public.tokens_id_seq'::regclass);
 8   ALTER TABLE public.tokens ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    218    217    218            q           2604    33713    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    212    211    212                      0    33701    bot 
   TABLE DATA           5   COPY public.bot (id, name_bot, nickname) FROM stdin;
    public          postgres    false    210   ,                 0    33771 
   chat_roles 
   TABLE DATA           ;   COPY public.chat_roles (id, id_chat, id_roles) FROM stdin;
    public          postgres    false    216   6,                 0    33756    roles 
   TABLE DATA           5   COPY public.roles (id_roles, name_roles) FROM stdin;
    public          postgres    false    214   �,                 0    42001    tokens 
   TABLE DATA           4   COPY public.tokens (id, token, id_user) FROM stdin;
    public          postgres    false    218   .                 0    33710    users 
   TABLE DATA           F   COPY public.users (id, name_user, nickname_user, id_chat) FROM stdin;
    public          postgres    false    212   P.       %           0    0 
   bot_id_seq    SEQUENCE SET     9   SELECT pg_catalog.setval('public.bot_id_seq', 1, false);
          public          postgres    false    209            &           0    0    chat_roles_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.chat_roles_id_seq', 10, true);
          public          postgres    false    215            '           0    0    roles_id_roles_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('public.roles_id_roles_seq', 13, true);
          public          postgres    false    213            (           0    0    tokens_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.tokens_id_seq', 7, true);
          public          postgres    false    217            )           0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 14, true);
          public          postgres    false    211            w           2606    33708    bot bot_pkey 
   CONSTRAINT     J   ALTER TABLE ONLY public.bot
    ADD CONSTRAINT bot_pkey PRIMARY KEY (id);
 6   ALTER TABLE ONLY public.bot DROP CONSTRAINT bot_pkey;
       public            postgres    false    210                       2606    33776    chat_roles chat_roles_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.chat_roles
    ADD CONSTRAINT chat_roles_pkey PRIMARY KEY (id);
 D   ALTER TABLE ONLY public.chat_roles DROP CONSTRAINT chat_roles_pkey;
       public            postgres    false    216            }           2606    33761    roles roles_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id_roles);
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public            postgres    false    214            �           2606    42007    tokens tokens_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.tokens DROP CONSTRAINT tokens_pkey;
       public            postgres    false    218            y           2606    33719    users users_nickname_user_key 
   CONSTRAINT     a   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_nickname_user_key UNIQUE (nickname_user);
 G   ALTER TABLE ONLY public.users DROP CONSTRAINT users_nickname_user_key;
       public            postgres    false    212            {           2606    33717    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    212            �           2606    33777 #   chat_roles chat_roles_id_roles_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.chat_roles
    ADD CONSTRAINT chat_roles_id_roles_fkey FOREIGN KEY (id_roles) REFERENCES public.roles(id_roles);
 M   ALTER TABLE ONLY public.chat_roles DROP CONSTRAINT chat_roles_id_roles_fkey;
       public          postgres    false    216    3197    214            �           2606    42008    tokens tokens_id_user_fkey    FK CONSTRAINT     y   ALTER TABLE ONLY public.tokens
    ADD CONSTRAINT tokens_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id);
 D   ALTER TABLE ONLY public.tokens DROP CONSTRAINT tokens_id_user_fkey;
       public          postgres    false    218    212    3195               #   x�3�t�/���K-����N�O�/����� ud�         d   x�-��� ��g9�����.(�ᨳU���I�t4�"+��	��*�4�koO{(e���X"G�x�T�a�-g'H�l�<�g�ť:s�puL�T�\�GD>?=�         N  x�mRIN�0<�_� "̰��p\�eADh�qA�E\��d��l��v$F(��vwuW��4x��bt�]���5��1�%��ú���=ȡ��	q�6j�@��5r92�t�K�"�i�
96�bE��#�<~"oS�Kt�.=��K�D?��('�lQ�J�������[�	�Rn�����p�s�)m˰� oC"a�?�F���Ԣ�PwKX�3PJx`��wZ&�����*c��I�=Vf��Y���F��v,o�Y�F}���I5���l�<�v���!�-f��B���j�y���JE�$�]Z��X��E���o3Z\�\�_^�ٞ�� _���         8   x�5ƹ�@�X*������qN��d(����$�ַ��cL��]�{H^;V	�         �  x�%P�J[A^�y�<��3w~��(��M� .W3�L�;7��JE�P"� "�)lQ�&��6�;t��s��|�-���"�UY &�pʤ҄A��w���0���S!�1Bi�$	��0��Ix~{گ�����0�)Fp¡�U{�u,le}�ڶ-�<1�j͑بG���d�}[2��0Rj"!�F#Ө�u^�ڛ ��F*Q�8�S���<��T	S	
A4,o��f�˳�����ߋ��b�cy5��6�|Z���׮�ރ��r��)���m��1�0\�e"�֫R��v
����_"�a,�&� ����"���D��J���b�ix����3?��`<��
�Fm�S�^��@�g��inK���
!�+���     